variable "dockerhub_login" {
    type=bool
    default=false
    description="Whether to login to DockerHub to prevent the pull limitation. Can be either false or true."
}

variable "dockerhub_username" {
    type=string
    default=null
    description="Username if you use DockerHub authentication."
}

variable "dockerhub_password" {
    type=string
    default=null
    description="Password if you use DockerHub authentication."
}

variable "poetry_version" {
    type=string
    default="1.1.14"
    description="Poetry version to install."
}

variable "docker_image_name" {
    type=string
    default="audiocodes-exporter"
}

variable "docker_tag" {
    type=string
    default="latest"
    description="Docker tag to use when building the Docker image."
}

variable "ecr_login" {
    type=bool
    default=false
    description="When pushing to ECR enable this and fill in the login_server."
}

variable "ecr_login_server" {
    type=string
    default=null
    description="Where to make ECR login calls, usually https://{account_number}.dkr.ecr.{aws_region}.amazonaws.com/"
}

source "docker" "alpine" {
    image = "python:alpine"
    commit = true
    changes = [
        # python:
        "ENV PYTHONFAULTHANDLER 1",
        "ENV PYTHONUNBUFFERED 1",
        "ENV PYTHONDONTWRITEBYTECODE 1",
        # Expose the port
        "EXPOSE 9954",
        # Set entrypoint
        "ENTRYPOINT [\"audiocodes-exporter\"]"
    ]
    login = var.dockerhub_login
    login_username = var.dockerhub_username
    login_password = var.dockerhub_password
}

build {
    sources = ["source.docker.alpine"]

    # Install Poetry
    provisioner "shell" {
        environment_vars = [
            "POETRY_VERSION=${var.poetry_version}",
            "POETRY_HOME=/etc/poetry",
        ]
        inline =[
            "apk --no-cache add curl",
            "curl -sSL https://install.python-poetry.org | python3 -",
        ]
    }

    # Copy build stuff
    provisioner "file" {
        sources=["poetry.lock","pyproject.toml","README.md"]
        destination="/tmp/"
    }

    provisioner "file" {
        source = "src/audiocodes_exporter"
        destination="/tmp/"
    }

    # Build application and install it
    provisioner "shell" {
        environment_vars=[
            "POETRY_NO_INTERACTION=1",
            "POETRY_VIRTUALENVS_CREATE=false",
            "PIP_NO_CACHE_DIR=1",
            "PIP_DISABLE_PIP_VERSION_CHECK=1",
            "PIP_DEFAULT_TIMEOUT=100",
        ]
        inline=[
            "cd /tmp",
            "/etc/poetry/bin/poetry build --format wheel",
            "pip install ./dist/audiocodes_exporter*.whl",
            "pip show audiocodes_exporter",
        ]
    }

    # Cleanup build stuff
    provisioner "shell" {
        inline=[
            "apk --purge del curl",
            "apk --purge del apk-tools",
        ]
    }

    post-processors {
        post-processor "docker-tag" {
            repository = var.docker_image_name
            tags = [var.docker_tag]
        }

        post-processor "docker-push" {
            ecr_login = var.ecr_login
            login_server = var.ecr_login_server
        }
    }
}