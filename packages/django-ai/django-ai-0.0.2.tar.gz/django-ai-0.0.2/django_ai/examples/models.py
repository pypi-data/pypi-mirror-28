# -*- coding: utf-8 -*-

import os

from django.db import models

if 'DJANGO_TEST' in os.environ:
    from django_ai.systems.spam_filtering.models import (
        IsSpammable,
        SpamFilterPreTraining,
    )
    APP_LABEL = "django_ai.examples"
else:  # pragma: no cover
    from systems.spam_filtering.models import (
        IsSpammable,
        SpamFilterPreTraining,
    )
    APP_LABEL = "examples"


class UserInfo(models.Model):
    """
    Example User Information Model
    """
    SEX_CHOICES = [(0, "M"), (1, "F")]

    age = models.IntegerField("Age")
    sex = models.SmallIntegerField("Sex", choices=SEX_CHOICES,
                                   blank=True, null=True)
    # -> Metrics
    avg1 = models.FloatField("Average 1", blank=True, null=True)
    avg_time_pages = models.FloatField("Average Time on Pages",
                                       default=0, blank=True, null=True)
    visits_pages = models.IntegerField("Visits on Pages (Total)",
                                       default=0)
    avg_time_pages_a = models.FloatField("Average Time on Pages of type A",
                                         default=0, blank=True, null=True)
    visits_pages_a = models.IntegerField("Visits on Pages of type A",
                                         default=0)
    avg_time_pages_b = models.FloatField("Average Time on Pages of type B",
                                         default=0, blank=True, null=True)
    visits_pages_b = models.IntegerField("Visits on Pages of type B",
                                         default=0)
    avg_time_pages_c = models.FloatField("Average Time on Pages of type C",
                                         default=0, blank=True, null=True)
    visits_pages_c = models.IntegerField("Visits on Pages of type C",
                                         default=0)
    avg_time_pages_d = models.FloatField("Average Time on Pages of type D",
                                         default=0, blank=True, null=True)
    visits_pages_d = models.IntegerField("Visits on Pages of type D",
                                         default=0)
    avg_time_pages_e = models.FloatField("Average Time on Pages of type E",
                                         default=0, blank=True, null=True)
    visits_pages_e = models.IntegerField("Visits on Pages of type E",
                                         default=0)
    avg_time_pages_f = models.FloatField("Average Time on Pages of type F",
                                         default=0, blank=True, null=True)
    visits_pages_f = models.IntegerField("Visits on Pages of type F",
                                         default=0)
    avg_time_pages_g = models.FloatField("Average Time on Pages of type G",
                                         default=0, blank=True, null=True)
    visits_pages_g = models.IntegerField("Visits on Pages of type G",
                                         default=0)
    avg_time_pages_h = models.FloatField("Average Time on Pages of type H",
                                         default=0, blank=True, null=True)
    visits_pages_h = models.IntegerField("Visits on Pages of type H",
                                         default=0)
    avg_time_pages_i = models.FloatField("Average Time on Pages of type I",
                                         default=0, blank=True, null=True)
    visits_pages_i = models.IntegerField("Visits on Pages of type I",
                                         default=0)
    avg_time_pages_j = models.FloatField("Average Time on Pages of type J",
                                         default=0, blank=True, null=True)
    visits_pages_j = models.IntegerField("Visits on Pages of type J",
                                         default=0)
    # -> Results
    cluster_1 = models.CharField("Cluster 1", max_length=1,
                                 blank=True, null=True)

    class Meta:
        verbose_name = "User Info"
        verbose_name_plural = "Users Infos"
        app_label = APP_LABEL

    def __str__(self):
        return("{} - S: {}, A:{} - Group: {}".format(
            self.id, self.get_sex_display(), self.age, self.cluster_1)
        )


class CommentOfMySite(IsSpammable):
    SPAM_FILTER = "Spam Filter for Comments (example)"
    SPAMMABLE_FIELD = "comment"

    comment = models.TextField("Comment")
    user_id = models.SmallIntegerField("User ID")

    class Meta:
        verbose_name = "Comment of my Site"
        verbose_name_plural = "Comments of my Site"
        app_label = APP_LABEL

    def __str__(self):
        return("[U: {}] {}...".format(self.user_id, self.comment[:20]))


class SFPTEnron(SpamFilterPreTraining):

    class Meta:
        verbose_name = "Spam Filter Pre-Training: Enron Email Data"
        verbose_name_plural = "Spam Filter Pre-Training: Enron Emails Data"
        app_label = APP_LABEL


class SFPTYoutube(SpamFilterPreTraining):

    class Meta:
        verbose_name = "Spam Filter Pre-Training: Youtube Comment Data"
        verbose_name_plural = ("Spam Filter Pre-Training: "
                               "Youtube Comments Data")
        app_label = APP_LABEL
