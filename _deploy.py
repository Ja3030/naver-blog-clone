#!/usr/bin/env python3
"""자동 배포 유틸리티 — git add + commit + push + vercel deploy
모든 _build_*.py 스크립트 끝에서 호출한다.

사용법:
  from _deploy import auto_deploy
  auto_deploy("peptide-cream-v2", "어드버토리얼 v2 업데이트")
"""

import subprocess
import sys
import os

REPO_DIR = os.path.dirname(os.path.abspath(__file__))

def run(cmd, cwd=None):
    result = subprocess.run(cmd, shell=True, cwd=cwd or REPO_DIR,
                          capture_output=True, text=True)
    return result.returncode, result.stdout.strip(), result.stderr.strip()

def auto_deploy(post_slug: str, message: str = ""):
    """빌드 후 자동으로 git push + vercel deploy 실행"""

    commit_msg = message or f"Update post: {post_slug}"
    post_path = f"public/posts/{post_slug}/"

    print(f"\n🚀 자동 배포 시작: {post_slug}")

    # 1. git add (해당 포스트 + 빌드 스크립트)
    code, out, err = run(f'git add "{post_path}"')
    if code != 0:
        print(f"❌ git add 실패: {err}")
        return False

    # 빌드 스크립트도 추가 (새로 생성된 경우)
    run(f'git add "_build_*.py" "_deploy.py"')

    # 2. 변경사항 확인
    code, out, err = run('git diff --cached --name-only')
    if not out:
        print("ℹ️  변경사항 없음 — 배포 스킵")
        return True

    print(f"📝 변경 파일:\n{out}")

    # 3. git commit
    code, out, err = run(f'git commit -m "{commit_msg}"')
    if code != 0:
        print(f"❌ git commit 실패: {err}")
        return False
    print(f"✅ 커밋 완료: {commit_msg}")

    # 4. git push
    code, out, err = run('git push')
    if code != 0:
        print(f"❌ git push 실패: {err}")
        return False
    print("✅ git push 완료")

    # 5. vercel deploy
    code, out, err = run('vercel --prod --yes')
    if code != 0:
        print(f"❌ vercel 배포 실패: {err}")
        return False

    # URL 추출
    for line in (out + '\n' + err).split('\n'):
        if 'vercel.app' in line and 'http' in line:
            url = line.strip().split()[-1]
            print(f"✅ Vercel 배포 완료: {url}")
            print(f"🔗 포스트: {url}/posts/{post_slug}/")
            print(f"🔧 어드민: {url}/admin/")
            break
    else:
        print("✅ Vercel 배포 완료")

    return True

if __name__ == "__main__":
    # 직접 실행 시: python3 _deploy.py <post_slug> [message]
    if len(sys.argv) < 2:
        print("Usage: python3 _deploy.py <post-slug> [commit message]")
        sys.exit(1)

    slug = sys.argv[1]
    msg = sys.argv[2] if len(sys.argv) > 2 else ""
    success = auto_deploy(slug, msg)
    sys.exit(0 if success else 1)
