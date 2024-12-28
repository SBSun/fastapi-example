from fastapi import HTTPException
from sqlalchemy.orm import joinedload, Query

from database import SessionLocal
from note.domain.note import Note as NoteVO
from note.domain.repository.note_repo import INoteRepository
from utils.db_utils import row_to_dict
from note.infra.db_models.note import Note, Tag

class NoteRepository(INoteRepository):
    def get_notes(
        self,
        user_id: str,
        page: int,
        items_per_page: int
    ) -> tuple[int, list[NoteVO]]:
        with SessionLocal() as db:
            # joinedload 함수를 이용해 조회할 때 연관 테이블의 데이터를 함께 가져온다.
            query: Query = (
                db.query(Note)
                .options(joinedload(Note.tags))
                .filter(Note.user_id == user_id)
            )

            total_count = query.count()
            notes = (
                query.offset((page - 1) * items_per_page)
                .limit(items_per_page).all()
            )

        note_vos = [NoteVO(**row_to_dict(note)) for note in notes]

        return total_count, note_vos

    def find_by_id(self, user_id: str, id: str) -> NoteVO:
        with SessionLocal() as db:
            note = (
                db.query(Note)
                .options(joinedload(Note.tags))
                .filter(Note.user_id == user_id, Note.id == id)
                .first()
            )

            if not note:
                raise HTTPException(status_code=422)

        return NoteVO(**row_to_dict(note))

    def save(self, user_id: str, note_vo: NoteVO) -> NoteVO:
        with SessionLocal() as db:
            tags: list[Tag] = []
            # 태그의 이름 여러 노트가 참조하며 유일한 값을 가진다.
            # 따라서 기존에 존재하는 태그인지 체크한다.
            for tag in note_vo.tags:
                existing_tag = db.query(Tag).filter(Tag.name == tag.name).first()
                if existing_tag:
                    tags.append(existing_tag)
                else:
                    tags.append(
                        Tag(
                            id=tag.id,
                            name=tag.name,
                            created_at=tag.created_at,
                            updated_at=tag.updated_at
                        )
                    )

            new_note = Note(
                id=note_vo.id,
                user_id=user_id,
                title=note_vo.title,
                content=note_vo.content,
                memo_date=note_vo.memo_date,
                tags=tags,
                created_at=note_vo.created_at,
                updated_at=note_vo.updated_at
            )

            db.add(new_note)
            db.commit()

            return NoteVO(**row_to_dict(new_note))

    def update(self, user_id: str, note_vo: NoteVO) -> NoteVO:
        with SessionLocal() as db:
            self.delete_tags(user_id, note_vo.id)

            note = (
                db.query(Note)
                .filter(Note.user_id == user_id, Note.id == note_vo.id)
                .first()
            )
            if not Note:
                raise HTTPException(status_code=422)

            note.title = note_vo.title
            note.content = note_vo.content
            note.memo_date = note_vo.memo_date

            tags: list[Tag] = []
            for tag in note_vo.tags:
                existing_tag = db.query(Tag).filter(Tag.name == tag.name).first()
                if existing_tag:
                    tags.append(existing_tag)
                else:
                    tags.append(
                        Tag(
                            id=tag.id,
                            name=tag.name,
                            created_at=tag.created_at,
                            updated_at=tag.updated_at
                        )
                    )

            note.tags = tags

            db.add(note)
            db.commit()

            return NoteVO(**row_to_dict(note))

    def delete(self, user_id: str, id: str):
        with SessionLocal() as db:
            self.delete_tags(user_id, id)

            note = (
                db.query(Note)
                .filter(Note.user_id == user_id, Note.id == id)
                .first()
            )
            if not Note:
                raise HTTPException(status_code=422)

            db.delete(note)
            db.commit()

    def delete_tags(self, user_id: str, id: str):
        with SessionLocal() as db:
            note = db.query(Note).filter(Note.user_id == user_id, Note.id == id).first()

            if not note:
                raise HTTPException(status_code=422)

            note.tags = []
            db.add(note)
            db.commit()

            # 사용되지 않는 태그 조회 후 삭제
            unused_tags = db.query(Tag).filter(~Tag.notes.any()).all()
            for tag in unused_tags:
                db.delete(tag)

            db.commit()

    def get_notes_by_tag_name(
        self,
        user_id: str,
        tag_name: str,
        page: int,
        items_per_page: int
    ) -> tuple[int, list[NoteVO]]:
        with SessionLocal() as db:
            tag = db.query(Tag).filter_by(name=tag_name).first()

            if not tag:
                return 0, []

            query: Query = (
                db.query(Note)
                # .options(joinedload(Note.tags))
                .filter(
                    Note.user_id == user_id,
                    Note.tags.any(id=tag.id)
                )
            )

            total_count = query.count()
            notes = (
                query.offset((page - 1) * items_per_page).limit(items_per_page).all()
            )

        note_vos = [NoteVO(**row_to_dict(note)) for note in notes]

        return total_count, note_vos