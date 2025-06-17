from django.urls import path
from .views import (
    LectureOnlyView,
    update_account,
    delete_account,
    LectureView,
    AssignmentListCreateView,
    AssignmentRetrieveUpdateDestroyView,
    AssignmentSubmissionListView,
    AssignmentSubmissionFeedbackView,
)

urlpatterns = [
    path('retrieve_user/<username>', LectureView.as_view({'get': 'retrieve'})),
    path("lecture_dashboard", LectureOnlyView.as_view()),
    path("update", update_account),
    path("delete", delete_account),
    path('assignments/', AssignmentListCreateView.as_view(), name='lecturer-assignment-list-create'),
    path('assignments/<int:pk>/', AssignmentRetrieveUpdateDestroyView.as_view(), name='lecturer-assignment-detail'),
    path('submissions/', AssignmentSubmissionListView.as_view(), name='lecturer-submission-list'),
    path('submissions/<int:pk>/feedback/', AssignmentSubmissionFeedbackView.as_view(), name='lecturer-submission-feedback'),
]