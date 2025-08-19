import os
import psutil
import tracemalloc
from certificate_generator import CertificateGenerator

def main():
    import test_single
    tracemalloc.start()
    snapshot_before = tracemalloc.take_snapshot()
    print("Memory snapshot taken before certificate generation.")
    # Run test_single.py logic (generates certificate)
    # test_single.py will execute on import
    snapshot_after = tracemalloc.take_snapshot()
    print("Memory snapshot taken after certificate generation.")
    stats = snapshot_after.compare_to(snapshot_before, 'filename')
    total_alloc = sum([stat.size_diff for stat in stats])
    print(f"Total memory allocated during certificate generation: {total_alloc} bytes ({total_alloc/1024:.2f} KB)")
    tracemalloc.stop()

if __name__ == "__main__":
    main()
