from django.shortcuts import render, redirect, get_object_or_404
from .models import Directory, File
from .forms import DirectoryForm, FileForm
from django.contrib import messages
from django_filters.views import FilterView
from .filters import FileFilter
from django.views.decorators.csrf import csrf_exempt

def directory_view(request, dir_id=None):
    directory = None
    if dir_id:
        directory = get_object_or_404(Directory, id=dir_id)
        subdirectories = Directory.objects.filter(parent=directory)
        files = File.objects.filter(directory=directory)
        parent_id = directory.pk  # Parent directory ID for new subdirectories
    else:
        subdirectories = Directory.objects.filter(parent=None)
        files = File.objects.filter(directory=None)
        parent_id = None

    context = {
        'current_directory': directory if dir_id else None,
        'subdirectories': subdirectories,
        'files': files,
        'dir_form': DirectoryForm(),
        'file_form': FileForm(),
        'parent_id': parent_id,
        'current_directory_id': directory.pk if directory else None,
    }
    return render(request, 'files/file.html', context)

def add_directory(request):
    if request.method == 'POST':
        form = DirectoryForm(request.POST)

        if form.is_valid():
            directory = form.save(commit=False)
            parent_id = request.POST.get('parent')

            # Debug print statements
            print("Parent ID from form:", parent_id)
            print("Form is valid. Directory name:", directory.name)

            # Determine if this is a root directory creation
            if not parent_id or parent_id in ['0', 'None', '', None]:  # Handle root directory creation
                directory.parent = None
            else:
                # Attempt to retrieve parent directory
                parent_directory = Directory.objects.filter(pk=parent_id).first()
                if parent_directory:
                    directory.parent = parent_directory
                else:
                    print("No valid parent found; creating as root directory.")
                    directory.parent = None  # Default to root if parent not found

            # Debug: Print the parent directory
            print("Resolved Parent Directory:", directory.parent)

            directory.save()

            # Redirect back to the appropriate view
            if directory.parent:
                return redirect('files:directory_view', dir_id=directory.parent.pk)
            return redirect('files:home')
        else:
            # Print form errors to debug why it's not valid
            print("Form is not valid. Errors:", form.errors)

            # Attempt to create a root directory if form is invalid
            # due to parent field issues
            if 'parent' in form.errors:
                print("Creating root directory as fallback.")
                directory = Directory(name=request.POST.get('name'), parent=None)
                directory.save()
                return redirect('files:home')

    else:
        # Debug: Log if the request method is not POST
        print("Request method is not POST.")

    return redirect('files:home')

def add_file(request):
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            # Ensure either file or URL is provided
            if not (file.file or file.url):
                form.add_error(None, "Either upload a file or provide a URL.")
            else:
                file.save()
                return redirect('files:home')
                
    return redirect('files:home')
    


def delete_directory(request, pk):
    directory = get_object_or_404(Directory, pk=pk)
    directory.delete()
    return redirect('files:home')

def delete_file(request, pk):
    file = get_object_or_404(File, pk=pk)
    file.delete()
    return redirect('files:file_listing')


class FileListView(FilterView):
    model = File
    template_name = 'files/file_list.html'
    context_object_name = 'files'
    filterset_class = FileFilter


def file_listing(request):
    files = File.objects.select_related('directory').all()
    return render(request, 'files/file_listing.html', {'files': files})


    
# Edit file name view
@csrf_exempt
def edit_file(request, file_id):
    file = get_object_or_404(File, pk=file_id)
    if request.method == 'POST':
        file.name = request.POST.get('name')
        file.owner = request.POST.get('owner')  # Update the owner field
        file.url = request.POST.get('url')
        file.save()
        return redirect('files:file_listing')

    return render(request, 'edit_file.html', {'file': file})
    