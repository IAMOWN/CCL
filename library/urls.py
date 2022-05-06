from django.urls import path

from .views import (
    TagList,
    TagDetail,
    TagCreate,
    TagUpdate,
    TagDelete,
    CosmicAuthorList,
    CosmicAuthorDetail,
    CosmicAuthorCreate,
    CosmicAuthorUpdate,
    CosmicAuthorDelete,
    LibraryRecordList,
    LibraryRecordDetail,
    LibraryRecordCreate,
    LibraryRecordUpdate,
    LibraryRecordDelete,
)

urlpatterns = [
    # Tags
    path('tags/', TagList.as_view(), name='tags'),
    path('tag/<int:pk>/', TagDetail.as_view(), name='tag'),
    path('tag_create/', TagCreate.as_view(), name='tag-create'),
    path('tag_update/<int:pk>/', TagUpdate.as_view(), name='tag-update'),
    path('tag_delete/<int:pk>/', TagDelete.as_view(), name='tag-delete'),

    # Authors
    path('authors/', CosmicAuthorList.as_view(), name='authors'),
    path('author/<int:pk>/', CosmicAuthorDetail.as_view(), name='author'),
    path('author_create/', CosmicAuthorCreate.as_view(), name='author-create'),
    path('author_update/<int:pk>/', CosmicAuthorUpdate.as_view(), name='author-update'),
    path('author_delete/<int:pk>/', CosmicAuthorDelete.as_view(), name='author-delete'),

    # Library Records
    path('library_records/', LibraryRecordList.as_view(), name='library-records'),
    path('library_record/<int:pk>/', LibraryRecordDetail.as_view(), name='library-record'),
    path('library_record_create/', LibraryRecordCreate.as_view(), name='library-record-create'),
    path('library_record_update/<int:pk>/', LibraryRecordUpdate.as_view(), name='library-record-update'),
    path('library_record_delete/<int:pk>/', LibraryRecordDelete.as_view(), name='library-record-delete'),
]
