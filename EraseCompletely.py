# EraseCompletely
import os
import sys
import secrets
import string

CHUNK_SIZE = 1024 * 1024  # 1MB単位で処理

def randomFileName(length=16):
    """ランダムなファイル名を生成"""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def overWriteSpecific(filePath, byteVal):
    """ファイル全体を指定のバイトで上書き"""
    contentLength = os.path.getsize(filePath)
    pattern = byteVal * CHUNK_SIZE
    with open(filePath, "r+b") as f:
        written = 0
        while written < contentLength:
            to_write = min(CHUNK_SIZE, contentLength - written)
            f.write(pattern[:to_write])
            written += to_write
        f.flush()
        os.fsync(f.fileno())  # ディスクへの書き込み保証

def overWriteRandom(filePath, passes=1):
    """ファイル全体をランダムデータで指定回数上書き"""
    contentLength = os.path.getsize(filePath)
    with open(filePath, "r+b") as f:
        for _ in range(passes):
            f.seek(0)
            written = 0
            while written < contentLength:
                to_write = min(CHUNK_SIZE, contentLength - written)
                f.write(secrets.token_bytes(to_write))
                written += to_write
            f.flush()
            os.fsync(f.fileno())  # ディスクへの書き込み保証

def eraseCompletely(filePath, random_passes=3):
    """ファイルを複数回上書きしてランダムリネーム後に削除"""
    if not os.path.exists(filePath):
        print(f"Error: File '{filePath}' does not exist.")
        return

    # 固定パターンで上書き
    overWriteSpecific(filePath, b'\x00')
    overWriteSpecific(filePath, b'\xff')
    # ランダムで指定回数上書き
    overWriteRandom(filePath, passes=random_passes)

    # ランダムファイル名にリネーム
    dirName = os.path.dirname(filePath) or "."
    random_name = randomFileName() 
    newPath = os.path.join(dirName, random_name)
    try:
        os.rename(filePath, newPath)
        filePath = newPath
    except Exception as e:
        print(f"Warning: Could not rename file before deletion: {e}")

    # ファイル削除
    os.remove(filePath)
    print(f"File has been securely erased (renamed to '{os.path.basename(filePath)}' before deletion).")

if __name__ == '__main__':
    args = sys.argv
    if len(args) == 2:
        eraseCompletely(args[1])
    elif len(args) == 3:
        try:
            passes = int(args[2])
        except ValueError:
            print("Error: random_passes must be an integer.")
            sys.exit(1)
        eraseCompletely(args[1], random_passes=passes)
    else:
        print("Usage: python EraseCompletely.py <filePath> [random_passes]")
