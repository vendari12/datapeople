from typing import List, Optional

from pydantic import BaseModel


class SingleJobSummary(BaseModel):
    role: str
    PostedDate: str

class OrganizationSummary(BaseModel):
    OrganizationName: str

class JobsSummary(BaseModel):
    NumberOfJobs: int
    OldestJob: Optional[SingleJobSummary]
    NewestJob: Optional[SingleJobSummary]

class OrganizationsSummary(BaseModel):
    NumberOfJobs: int
    NumberOfOrganizations: int
    OrganizationNames: List[OrganizationSummary]