import os
import json
import matplotlib
matplotlib.use('Agg')  # 🔥 Обязательно для Docker (без GUI)
import matplotlib.pyplot as plt
from datetime import datetime

def create_manifest():
    """Создаёт цифровую подпись выполнения"""
    is_docker = os.path.exists('/.dockerenv')
    manifest = {
        "timestamp": datetime.utcnow().isoformat(),
        "hostname": os.uname().nodename,
        "container": f"lab-13-{os.getenv('STUDENT_ID', 'unknown')}",
        "env": "docker" if is_docker else "local",
        "student_id": os.getenv('STUDENT_ID', 'unknown'),
        "lab_number": os.getenv('LAB_NUMBER', '13')
    }
    
    os.makedirs('/app/output', exist_ok=True)
    with open('/app/output/execution_manifest.json', 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2)
    print("✅ Manifest created: /app/output/execution_manifest.json")

def generate_trajectory():
    student_id = os.getenv('STUDENT_ID', 'unknown')
    pos_file = f'/app/workspace/mission_positions_{student_id}.json'
    log_file = f'/app/workspace/log_{student_id}.json'

    if not os.path.exists(pos_file):
        print(f"⚠️ Файл позиций не найден: {pos_file}")
        return

    with open(pos_file, 'r', encoding='utf-8') as f:
        positions = json.load(f)

    x = [p.get('x', 0) for p in positions]
    y = [p.get('y', 0) for p in positions]

    plt.figure(figsize=(10, 6))
    plt.plot(x, y, marker='.', linestyle='-', linewidth=1.5, label='trajectory')
    plt.scatter([x[0]], [y[0]], c='green', label='start', s=100, zorder=5)
    plt.scatter([x[-1]], [y[-1]], c='blue', label='end', s=100, zorder=5)

    # Отметка коллизий из логов
    if os.path.exists(log_file):
        with open(log_file, 'r', encoding='utf-8') as f:
            logs = json.load(f)
        collisions = [l for l in logs if l.get('type') == 'collision']
        if collisions:
            plt.scatter([c.get('x') for c in collisions], 
                        [c.get('y') for c in collisions], 
                        c='red', label='collisions', s=80, zorder=4)

    plt.title(f'Trajectory with collisions | Student: {student_id}')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend()
    plt.grid(True, alpha=0.6)
    plt.tight_layout()

    os.makedirs('/app/output', exist_ok=True)
    output_path = f'/app/output/traject_{student_id}.png'
    plt.savefig(output_path, dpi=150)
    plt.close()
    print(f"✅ Graph saved: {output_path}")

if __name__ == "__main__":
    print(f"🚀 Starting analysis for {os.getenv('STUDENT_ID')}...")
    create_manifest()
    generate_trajectory()
    print("✅ Analysis complete. Check /app/output/ on host.")
