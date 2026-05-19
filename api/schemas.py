from pydantic import BaseModel
from typing import Optional


class SearchRequest(BaseModel):
    query: str
    min_experience: Optional[int]  = None   # filter: minimum years of experience
    location:       Optional[str]  = None   # filter: candidate location


class CandidateResult(BaseModel):
    rank:             int
    similarity_score: float
    sandbox_link:     str
    candidate_name:   str
    matched_skills:   list[str]
    experience_years: int
    location:         str
    file_name:        str


class SearchResponse(BaseModel):
    original_query:  str
    understood_as:   str
    search_query:    str
    filters_applied: dict
    total_results:   int
    results:         list[CandidateResult]