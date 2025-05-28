from django.shortcuts import HttpResponse
from django.template import loader
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Max

from .forms import PathForm, PathPointForm, BoardForm, GameBoard, BoardPointsForm
from .models import Background, Path, Point, Dot
from .serializers import BoardPointsListSerializer

def home(request):
    if request.user.is_authenticated:
        return render(request, 'Paths/main.html', {
            'user': request.user
        })
    return render(request, 'Paths/home.html')

def background_show(request):
    background_list = Background.objects.all()
    template = loader.get_template("Paths/index.html")
    context = {"bg_list": background_list}
    return render(request, "Paths/index.html", context)

@login_required
def select_background(request):
    bgs = Background.objects.all()
    user_profile = request.user.profile

    if request.method == 'POST':
        background_id = request.POST.get('background_id')
        if not background_id:
            user_profile.selected_background = None
            user_profile.save()
            return redirect('path_list')
        
        selected_bg = Background.objects.get(id=background_id)
        user_profile.selected_background = selected_bg
        user_profile.save()
        return redirect('path_list')



    return render(request, 'Paths/bg_select.html', {
        'backgrounds': bgs,
        'current_background': user_profile.selected_background
    })

@login_required
def path_list(request):
    user = request.user
    profile = user.profile
    selected_background = profile.selected_background

    paths = Path.objects.filter(user=user, background=selected_background)

    if request.method == 'POST':
        if not selected_background:
            return redirect('select_background')

        path_form = PathForm(request.POST)
        if path_form.is_valid():
            new_path = path_form.save(commit=False)
            new_path.user = user
            new_path.background = selected_background
            new_path.save()
            return redirect('path_detail', path_id=new_path.id)
    else:
        path_form = PathForm()

    context = {
        'paths': paths,
        'selected_background': selected_background,
        'path_form': path_form,
    }
    return render(request, 'Paths/path_list.html', context)

@login_required
def path_create(request):
    if request.method == 'POST':
        form = PathForm(request.POST)
        if form.is_valid():
            path = form.save(commit=False)
            path.user = request.user
            path.background = request.user.profile.selected_background
            path.save()
            return redirect('path_detail', path_id=path.id)
    else:
        form = PathForm()
    return render(request, 'Paths/path_form.html', {'form': form})

@login_required
def path_detail(request, path_id):
    path = get_object_or_404(Path, id=path_id, user=request.user)
    points = path.points.order_by('order')
    point_form = PathPointForm(request.POST)
    if request.method == 'POST':
        if point_form.is_valid():
            last_point_order = points.aggregate(Max('order'))['order__max']
            next_order = (last_point_order or 0) + 1

            new_point = point_form.save(commit=False)
            new_point.path = path
            new_point.order = next_order
            new_point.save()
            return redirect('path_detail', path_id=path.id)

    return render(request, 'Paths/path_detail.html', {
        'path': path,
        'points': points,
        'point_form': point_form,
        'background': path.background
    })

@login_required
def point_add(request, path_id):
    path = get_object_or_404(path, id=path_id, user=request.user)
    if request.method == 'POST':
        form = PathPointForm(request.POST)
        if form.is_valid():
            point = form.save(commit=False)
            point.path = path
            point.save()
    return redirect('path_detail', path_id=path.id)

@login_required
def point_delete(request, point_id):
    point = get_object_or_404(Point, id=point_id)
    if point.path.user != request.user:
        return redirect('path_list')
    path_id = point.path.id
    point.delete()
    return redirect('path_detail', path_id=path_id)

@login_required
def delete_path(request, path_id):
    path = get_object_or_404(Path, id=path_id, user=request.user)
    path_name = path.name
    if request.method == 'POST':
        path.delete()
        return redirect('path_list')
    return redirect('path_list')


@login_required
def board_create(request): 
    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            board = form.save(commit=False)
            board.user = request.user
            board.name = form.cleaned_data['name']
            board.rows = form.cleaned_data['rows']
            board.cols = form.cleaned_data['cols']
            board.save()
            return redirect('board_detail', board_id=board.id)
    else:
        form = BoardForm()
    return render(request, 'Paths/board_form.html', {'form': form})

@login_required
def board_detail(request, board_id):
    board = get_object_or_404(GameBoard, id=board_id, user=request.user)
    dots = board.dots.all()

    if request.method == 'POST':
        board_form = BoardPointsForm(request.POST)
        if board_form.is_valid():
            points_data = board_form.cleaned_data['points']
            board.dots.all().delete()

            
            points = points_data
            for point in points:
                dot = Dot()
                dot.row = point['row']
                dot.col = point['col']
                dot.color = point['color']
                dot.board = board
                dot.save()
            return redirect('board_detail', board_id=board_id)
    board_form = BoardForm()

    return render(request, 'Paths/board_detail.html', {
        'board': board,
        'dots': dots,
        'cols': board.cols,
        'rows': board.rows,
        'board_form': board_form,
    })


@login_required
def board_list(request):
    user = request.user
    boards = GameBoard.objects.filter(user=user)

    context = {
        'boards': boards,
    }
    return render(request, 'Paths/board_list.html', context)
    


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
