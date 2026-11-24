"""사용자별 번호(user_no) 추가. 이미 있는 작업은 사용자마다 만든 순서대로 1, 2, 3…을 채웁니다."""
from django.db import migrations, models


def fill_user_no(apps, schema_editor):
    AnalysisJob = apps.get_model("analyses", "AnalysisJob")
    counters = {}
    for job in AnalysisJob.objects.order_by("user_id", "created_at", "id"):
        counters[job.user_id] = counters.get(job.user_id, 0) + 1
        job.user_no = counters[job.user_id]
        job.save(update_fields=["user_no"])


class Migration(migrations.Migration):

    dependencies = [
        ("analyses", "0002_video_meta_and_details"),
    ]

    operations = [
        migrations.AddField(
            model_name="analysisjob",
            name="user_no",
            field=models.PositiveIntegerField(blank=True, editable=False, null=True, verbose_name="사용자별 번호"),
        ),
        migrations.RunPython(fill_user_no, migrations.RunPython.noop),
    ]
