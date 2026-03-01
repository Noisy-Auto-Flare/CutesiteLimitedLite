# Cutesite

Cutesite is a fully containerized, production-ready web application designed for sharing images, videos, and text posts. It features a clean, "cute" pastel aesthetic and robust backend architecture.

## 🌟 Key Features

### 🖼️ Image Gallery
- **Upload**: Support for common image formats (JPEG, PNG, GIF, WEBP).
- **Management**: View in a responsive grid, download, share via link, and delete.
- **Fullscreen Mode**: Click any image to view it in a high-resolution modal.
- **Auto-Cleanup**: Automatically maintains a fixed number of recent images (default: 50) to save space.

### 🎥 Video Player
- **Upload**: Support for short video clips (MP4, WEBM).
- **Constraints**: Enforces limits on file size (100MB) and duration (60s).
- **Player**: Built-in video player with fullscreen support.
- **Auto-Cleanup**: Keeps only the most recent videos (default: 15).

### 📝 Text Posts
- **Publishing**: Create and share thoughts with optional titles.
- **Feed**: Chronological feed of posts.
- **Auto-Cleanup**: Maintains a history of recent posts (default: 50).

### 📱 Mobile-First Design
- **Responsive**: Seamless experience across desktop, tablet, and mobile.
- **Navigation**: Sticky bottom navigation bar for easy access on mobile devices.
- **Touch Friendly**: Large touch targets and intuitive interactions.

## 🏗️ Architecture

- **Backend**: Python (FastAPI) - High performance, easy to maintain.
- **Frontend**: TypeScript (Next.js) - Server-side rendering, modern React patterns.
- **Database**: PostgreSQL - Reliable relational data storage.
- **Proxy**: Caddy - Automatic HTTPS and reverse proxying.
- **Containerization**: Docker & Docker Compose - One-command deployment.

## 💻 System Requirements

To run Cutesite effectively, ensure your system meets the following minimum requirements:

- **OS**: Linux, macOS, or Windows (with WSL2)
- **CPU**: 2 vCPUs recommended
- **RAM**: 2GB minimum (4GB recommended)
- **Disk Space**: 10GB free space (plus storage for uploads)
- **Software**:
  - Docker Engine 20.10+
  - Docker Compose v2.0+

## 🚀 Quick Start

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/cutesite.git
    cd cutesite
    ```

2.  **Configure Environment**:
    Copy the example configuration file:
    ```bash
    cp .env.example .env
    ```
    *Optional: Edit `.env` to customize limits (e.g., `MAX_IMAGES`, `MAX_VIDEOS`).*

3.  **Launch**:
    Build and start the services:
    ```bash
    docker compose up -d --build
    ```

4.  **Access**:
    Open your browser and navigate to: `http://localhost`

## ⚙️ Configuration

All settings are managed via the `.env` file.

| Variable | Description | Default |
|----------|-------------|---------|
| `APP_PORT` | Port exposed by Caddy | 80 |
| `MAX_IMAGES` | Maximum number of stored images | 50 |
| `MAX_VIDEOS` | Maximum number of stored videos | 15 |
| `MAX_POSTS` | Maximum number of stored posts | 50 |
| `MAX_VIDEO_SIZE_MB` | Max video file size in MB | 100 |
| `MAX_VIDEO_DURATION_SECONDS` | Max video length in seconds | 60 |
| `POSTGRES_USER` | Database username | postgres |
| `POSTGRES_PASSWORD` | Database password | postgres |
| `POSTGRES_DB` | Database name | cutesite |
| `DATABASE_URL` | SQLAlchemy connection string | postgresql://... |

## 🛠️ Maintenance

**Manual Cleanup**:
To manually trigger the cleanup script (deletes old files exceeding limits):
```bash
docker compose exec backend python scripts/cleanup.py
```

**Logs**:
View logs for all services:
```bash
docker compose logs -f
```
