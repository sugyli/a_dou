from django.views.generic import DetailView

from novels.models import Novel,Chapter

class NovelDetailView(DetailView):
    model = Novel
    template_name="novels/novel_detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(NovelDetailView, self).get_context_data(*args, **kwargs)
        sections = []
        chapters = Chapter.objects.filter(novel=context['novel'])
        for chapter in chapters:
            subsection={
                'sectionname': '默认分卷',
                'chapter': []
            }
            if not len(sections):
                if chapter.is_tab==True:
                    subsection['sectionname']=chapter.name
                else:
                    subsection['chapter'].append(chapter)
                sections.append(subsection)
            else:
                if chapter.is_tab==True:
                    subsection['sectionname'] = chapter.name
                    sections.append(subsection)
                else:
                    subsection=sections[-1]
                    subsection['chapter'].append(chapter)

        context['sections'] = sections
        context['lastchapter'] = None
        if chapters.count()>0:
            context['lastchapter'] = chapters.last()
        return context

    def get_queryset(self, **kwargs):
        return Novel.objects.get_published()


class ChapterDetailView(DetailView):
    model=Chapter
    template_name="novels/chapter_detail.html"

    def get_context_data(self, *args, **kwargs):
        context=super(ChapterDetailView, self).get_context_data(*args, **kwargs)

        context['nextchapter'] = \
            Chapter.objects.filter(order__gt=context['chapter'].order).first()
        context['prevchapter']= \
            Chapter.objects.filter(order__lt=context['chapter'].order).first()

        context['contentobj']= context['chapter'].get_chapter_content()

        return context


    def get_queryset(self, **kwargs):
        return Chapter.objects.get_published()
