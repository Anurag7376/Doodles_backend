from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.http import StreamingHttpResponse
from apps.agents.research_orchestrator import run_autonomous_research


class InteractiveResearchView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_input = request.data.get("message")

        # You can improve this with real session logic later
        session = None  

        def generate_stream():
            result = run_autonomous_research(session, user_input)
            yield str(result)

        return StreamingHttpResponse(generate_stream(), content_type="text/plain")
