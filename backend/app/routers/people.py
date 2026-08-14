from fastapi import APIRouter, HTTPException

from app.models import Person, PersonProfile
from app.queries import people as people_q

router = APIRouter(prefix="/api/people", tags=["people"])


@router.get("", response_model=list[Person])
def list_people():
    return people_q.list_people()


@router.get("/{person_id}", response_model=PersonProfile)
def get_person(person_id: str):
    person = people_q.get_person_profile(person_id)
    if person is None:
        raise HTTPException(status_code=404, detail=f"Person '{person_id}' not found")
    return person
