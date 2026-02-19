from django.http import StreamingHttpResponse
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from apps.agents.research_orchestrator import run_autonomous_research
from apps.chat.models import ChatSession


class InteractiveResearchView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user_input = request.data.get("message", "")

        session = None
        if request.user and request.user.is_authenticated:
            session, _ = ChatSession.objects.get_or_create(user=request.user)

        def generate_stream():
            result = run_autonomous_research(session, user_input)
            yield str(result)

        return StreamingHttpResponse(generate_stream(), content_type="text/plain")
