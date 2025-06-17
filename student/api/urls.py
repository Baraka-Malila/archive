from django.urls import path
from .views import (
    StudentOnlyView,
    update_account,
    delete_account,
    StudentAssignmentSubmissionListCreateView,
    StudentAssignmentSubmissionDetailView,
    StudentResourceListView,
    ResourceDownloadView,
)

urlpatterns = [
    path("student_dashboard", StudentOnlyView.as_view()),
    path("update", update_account),
    path("delete", delete_account),
    path('submissions/', StudentAssignmentSubmissionListCreateView.as_view(), name='student-submission-list-create'),
    path('submissions/<int:pk>/', StudentAssignmentSubmissionDetailView.as_view(), name='student-submission-detail'),
    path('resources/', StudentResourceListView.as_view(), name='student-resource-list'),
    path('resources/download/<int:pk>/', ResourceDownloadView.as_view(), name='student-resource-download'),
]
