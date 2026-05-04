from django.db import models
from django.db.models import Count


class LoanQuerySet(models.QuerySet):
    def active(self):
        return self.filter(status='active')

    def for_member(self, member):
        return self.filter(member=member)


class LoanManager(models.Manager):
    def get_queryset(self):
        return LoanQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()

    def for_member(self, member):
        return self.get_queryset().for_member(member)


class BookQuerySet(models.QuerySet):
    def available(self):
        return self.filter(is_available=True)

    def by_genre(self, genre):
        return self.filter(genre__iexact=genre)

    def popular(self):
        return self.annotate(borrow_count=Count('loans')).order_by('-borrow_count')


class BookManager(models.Manager):
    def get_queryset(self):
        return BookQuerySet(self.model, using=self._db)

    def available(self):
        return self.get_queryset().available()

    def by_genre(self, genre):
        return self.get_queryset().by_genre(genre)

    def popular(self):
        return self.get_queryset().popular()