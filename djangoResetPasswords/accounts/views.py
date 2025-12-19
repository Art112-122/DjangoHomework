from django.http import HttpResponse
from django.shortcuts import redirect

def visit_counter(request):
    visit_count = request.session.get("visit_count", 0)
    visit_count += 1
    request.session["visit_count"] = visit_count

    return HttpResponse(f"You have visited this page {visit_count} times")

def reset_visit_counter(request):
    request.session.pop("visit_count", None)
    return redirect("visit_counter")
