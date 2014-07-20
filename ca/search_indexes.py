import datetime
from haystack import indexes
from ca.models import Program


class ProgramIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)
    degree = indexes.CharField(model_attr="degree", faceted=True)
    university = indexes.CharField(model_attr='university', faceted=True)
    major = indexes.CharField(model_attr="major", faceted=True)
    academic_professional = indexes.CharField(model_attr="academic_professional", faceted=True)
    content_auto = indexes.EdgeNgramField(model_attr="name")

    def get_model(self):
        return Program

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
