from typing import List, Union
from pydantic import BaseModel

class StatCard(BaseModel):
    id: str
    title: str
    value: Union[int, str]
    icon: str
    change: str
    theme: str

class MonthlyRegistrationPoint(BaseModel):
    month: str
    count: int

class AdminRegistrationTrendPoint(BaseModel):
    month: str
    registrations: int

class CategoryDistributionPoint(BaseModel):
    name: str
    percentage: int
    color: str

class OrganizerAnalyticsResponse(BaseModel):
    stats: List[StatCard]
    chartData: List[MonthlyRegistrationPoint]

class AdminAnalyticsResponse(BaseModel):
    stats: List[StatCard]
    lineChartData: List[AdminRegistrationTrendPoint]
    categoryData: List[CategoryDistributionPoint]
