from django.db import models
from django.urls import reverse

from datetime import date

# ####################### Date logic #######################
def current_year():
    return date.today().year


# ####################### Cosmic Author #######################
class CosmicAuthor(models.Model):
    """Cosmic Authors are associated with library records."""
    author = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        default=''
    )

    # Record metadata
    date_created = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = [
            'author',
        ]

    def __str__(self):
        return self.author

    def get_absolute_url(self):
        return reverse('author', kwargs={'pk': self.pk})


# ####################### Tag #######################
class Tag(models.Model):
    """Tags are associated with library records."""
    tag = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        default=''
    )

    # Record metadata
    date_created = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = [
            'tag',
        ]

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse('tag', kwargs={'pk': self.pk})


# ####################### Library Record #######################
class LibraryRecord(models.Model):
    """Library records capture all Discourses for the CCL Web Application."""
    title = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        default=''
    )
    part_number = models.IntegerField(
        default=1
    )
    invocation = models.TextField(
        default='',
        blank=True,
        null=True,
    )
    body = models.TextField(
        default='',
        blank=True,
        null=True,
    )
    benediction = models.TextField(
        default='',
        blank=True,
        null=True,
    )
    series_title = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        default=''
    )
    principal_cosmic_author = models.ForeignKey(
        CosmicAuthor,
        related_name='principal_cosmic_author',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    supporting_cosmic_authors = models.ManyToManyField(
        CosmicAuthor,
        null=True,
        blank=True,
    )
    tags = models.ManyToManyField(
        Tag,
        null=True,
        blank=True,
    )
    date_communicated = models.DateField(default=date.today)
    year_communicated = models.IntegerField(default=current_year())
    pdf_url = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        default=''
    )
    doc_url = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        default=''
    )
    mp3_url = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        default=''
    )

    # Record metadata
    date_created = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = [
            'series_title',
            'part_number',
        ]

    def __str__(self):
        # return self.title
        return f'Part {self.part_number} - {self.series_title} - {self.title} - {self.principal_cosmic_author} - {self.date_communicated}'

    def get_absolute_url(self):
        return reverse('library-record', kwargs={'pk': self.pk})
