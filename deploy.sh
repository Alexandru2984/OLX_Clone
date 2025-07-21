#!/bin/bash
# Script de deploy automat pentru OLX Clone

echo "🚀 Starting OLX Clone deployment process..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if virtual environment exists
if [ ! -d "venv" ] && [ ! -d "myproject_venv" ]; then
    print_warning "Virtual environment not found. Creating one..."
    python3 -m venv venv
    source venv/bin/activate
else
    if [ -d "myproject_venv" ]; then
        source myproject_venv/bin/activate
        print_status "Activated myproject_venv virtual environment"
    else
        source venv/bin/activate
        print_status "Activated venv virtual environment"
    fi
fi

# Install/update dependencies
print_status "Installing dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    print_error "Failed to install dependencies"
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    print_warning ".env file not found. Copying from .env.example..."
    if [ -f ".env.example" ]; then
        cp .env.example .env
        print_warning "Please edit .env file with your actual values before running the server!"
    else
        print_error ".env.example not found. Please create .env file manually."
    fi
fi

# Run migrations
print_status "Running database migrations..."
python manage.py makemigrations
python manage.py migrate

if [ $? -ne 0 ]; then
    print_error "Migration failed"
    exit 1
fi

# Collect static files
print_status "Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser if it doesn't exist
print_status "Checking for superuser..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    print('No superuser found. Please create one:')
    exit(1)
" 2>/dev/null

if [ $? -eq 1 ]; then
    print_warning "No superuser found. Creating one..."
    python manage.py createsuperuser
fi

# Check if port is specified
PORT=${1:-8000}

print_status "Deployment completed successfully!"
print_status "Starting development server on port $PORT..."
print_warning "For production, use: gunicorn olx_clone.wsgi:application --bind 0.0.0.0:$PORT"

# Start development server
python manage.py runserver 0.0.0.0:$PORT
