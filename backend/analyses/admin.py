from django.contrib import admin

from .models import AnalysisJob, PersonPrediction


class PersonPredictionInline(admin.TabularInline):
    model = PersonPrediction
    extra = 0
    can_delete = False
    fields = ("track_id", "action_label", "raw_label", "confidence", "margin", "valid_frames", "input_quality")
    readonly_fields = fields


@admin.register(AnalysisJob)
class AnalysisJobAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "user_no", "input_type", "status", "expected_action", "prediction_summary", "processing_ms", "created_at")
    list_filter = ("status", "input_type", "expected_action", "created_at")
    search_fields = ("user__username", "title", "memo", "celery_task_id")
    # 상태·AI 결과는 Celery Worker만 저장합니다. 관리자는 제목·메모만 고칠 수 있습니다.
    readonly_fields = ("user", "user_no", "input_type", "video", "camera_index", "capture_seconds", "expected_action",
                       "status", "error_message", "result_message", "celery_task_id", "video_meta",
                       "started_at", "completed_at", "created_at", "processing_ms", "video_duration_sec")
    inlines = [PersonPredictionInline]
    date_hierarchy = "created_at"

    @admin.display(description="사람별 결과")
    def prediction_summary(self, obj):
        return ", ".join(f"#{p.track_id} {p.action_label}" for p in obj.predictions.all()) or "-"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("user").prefetch_related("predictions")

    def has_add_permission(self, request):
        # Admin에서 만든 작업은 Celery에 등록되지 않아 대기 상태로 멈추므로, 분석 요청은 서비스 화면에서만 받습니다.
        return False


@admin.register(PersonPrediction)
class PersonPredictionAdmin(admin.ModelAdmin):
    list_display = ("id", "job", "track_id", "action_label", "confidence", "margin", "input_quality", "predicted_at")
    list_filter = ("action_label", "input_quality", "job__input_type")
    search_fields = ("job__user__username", "action_label")
    list_select_related = ("job",)

    # AI 추론 결과는 조회만 (추가·수정 불가, 잘못된 기록 정리를 위해 삭제는 허용)
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
