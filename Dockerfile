FROM python:3.10

SHELL ["/bin/bash", "-c"]

WORKDIR /app

COPY . .

# Install the virtual environment
RUN pip install virtualenv

# Create the virtual environment
RUN python3 -m venv .venv

# Activate the virtual environment
RUN . .venv/bin/activate

# Install the Django app dependencies
RUN pip install -r requirements.txt

# Expose the Django development server port
EXPOSE 8000

# Start the Django development server
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
