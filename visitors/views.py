from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required 
from django.utils import timezone
# Import TimeSlot here
from .models import Student, VisitRequest, TimeSlot 

# 1. PARENT / STUDENT LOGIN (Keep as is)
def parent_login(request):
    error_message = None 
    if request.method == "POST":
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(request, username=u, password=p)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            error_message = "❌ Access Denied: Incorrect ID or Password."
    return render(request, 'login.html', {'error_message': error_message})

# 2. DASHBOARD (Fixed to pass available_slots)
@login_required(login_url='/')
def dashboard(request):
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        return render(request, 'dashboard.html', {'error': 'Student profile not found.'})

    last_visit = VisitRequest.objects.filter(student=student).last()
    
    # ADD THIS: Get active slots for the frontend dropdown
    available_slots = TimeSlot.objects.filter(is_active=True)
    
    if request.method == "POST":
        reason = request.POST.get('reason')
        slot_id = request.POST.get('time_slot') # Now receiving the ID
        
        selected_slot = get_object_or_404(TimeSlot, id=slot_id)
        
        VisitRequest.objects.create(
            student=student, 
            reason=reason, 
            time_slot=selected_slot, # Linking the object
            status='PENDING'
        )
        return redirect('dashboard')

    return render(request, 'dashboard.html', {
        'student': student,
        'visit': last_visit,
        'available_slots': available_slots, # Send to HTML
    })

# 3. ADMIN DASHBOARD (Fixed to handle slot creation)
@staff_member_required
def admin_dashboard(request):
    # ADD THIS: Logic to create a new slot
    if request.method == "POST" and 'add_slot' in request.POST:
        label = request.POST.get('label')
        start = request.POST.get('start_time')
        end = request.POST.get('end_time')
        
        TimeSlot.objects.create(
            label=label,
            start_time=start,
            end_time=end
        )
        return redirect('admin_dashboard')

    # Handle Approvals
    if request.method == "POST" and 'approve_id' in request.POST:
        v_id = request.POST.get('approve_id')
        visit = get_object_or_404(VisitRequest, id=v_id)
        visit.status = 'APPROVED'
        visit.save()
        return redirect('admin_dashboard')

    pending_requests = VisitRequest.objects.filter(status='PENDING')
    # ADD THIS: Fetch all slots to display in the list
    all_slots = TimeSlot.objects.all().order_by('start_time')
    
    return render(request, 'admin_dashboard.html', {
        'pending_requests': pending_requests,
        'all_slots': all_slots, # Send to HTML
    })

# 4. SECURITY SCANNER (Keep as is)
def scan_qr(request, visit_id):
    visit = get_object_or_404(VisitRequest, id=visit_id)
    msg = ""
    if visit.status == 'APPROVED':
        visit.status = 'INSIDE'
        visit.entry_time = timezone.now()
        msg = "✅ ENTRY APPROVED: Student Allowed In!"
    elif visit.status == 'INSIDE':
        visit.status = 'COMPLETED'
        visit.exit_time = timezone.now()
        msg = "👋 EXIT APPROVED: Visit Completed!"
    elif visit.status == 'COMPLETED':
        msg = "❌ EXPIRED: This QR has already been used."
    elif visit.status == 'PENDING':
        msg = "⚠️ PENDING: Admin has not approved this yet."
    visit.save()
    return render(request, 'scan_result.html', {'message': msg, 'visit': visit})

# 5. LOGOUT
def logout_view(request):
    logout(request)
    return redirect('/')