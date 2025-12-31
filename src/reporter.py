import os
import shutil
import hashlib
import subprocess
from collections import defaultdict
from src.utils import format_size, logger

class SystemReporter:
    def get_system_metrics(self):
        """Retrieves CPU and RAM usage using standard libraries."""
        metrics = {}
        try:
            # CPU and RAM are hard to get accurately cross-platform with just stdlib without psutil.
            # We will use os-specific commands/APIs if possible, or simplified placeholders.
            
            # Disk Usage (Standard Library)
            # shutil.disk_usage is available in Python 3.3+
            
            # RAM
            if os.name == 'nt':
                # Windows specific via ctypes kernel32 (simplified)
                import ctypes
                class MEMORYSTATUS(ctypes.Structure):
                    _fields_ = [
                        ("dwLength", ctypes.c_ulong),
                        ("dwMemoryLoad", ctypes.c_ulong),
                        ("ullTotalPhys", ctypes.c_ulonglong),
                        ("ullAvailPhys", ctypes.c_ulonglong),
                        ("ullTotalPageFile", ctypes.c_ulonglong),
                        ("ullAvailPageFile", ctypes.c_ulonglong),
                        ("ullTotalVirtual", ctypes.c_ulonglong),
                        ("ullAvailVirtual", ctypes.c_ulonglong),
                        ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
                    ]
                
                stat = MEMORYSTATUS()
                stat.dwLength = ctypes.sizeof(MEMORYSTATUS)
                ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat))
                
                metrics['ram_total'] = format_size(stat.ullTotalPhys)
                metrics['ram_available'] = format_size(stat.ullAvailPhys)
                metrics['ram_usage'] = f"{stat.dwMemoryLoad}%"
                
                # CPU via WMIC
                try:
                    # wmic cpu get loadpercentage
                    output = subprocess.check_output('wmic cpu get loadpercentage', shell=True)
                    # Output looks like "LoadPercentage \n 12 \n\n"
                    load = output.decode().splitlines()[1].strip()
                    metrics['cpu_usage'] = f"{load}%"
                except Exception:
                    metrics['cpu_usage'] = "N/A (WMIC failed)"
            else:
                # Linux/Mac fallback (reading /proc/meminfo or similar)
                # Simplified for this context since target is Windows
                metrics['ram_total'] = "N/A"
                metrics['ram_available'] = "N/A" 
                metrics['ram_usage'] = "N/A"
                metrics['cpu_usage'] = "N/A"

        except Exception as e:
            logger.error(f"Error getting system metrics: {e}")
            metrics['error'] = str(e)
        return metrics

    def get_disk_usage(self):
        """Retrieves disk usage for the main drive."""
        usage_info = {}
        try:
            # Check C: on Windows, or / on Linux
            drive = 'C:\\' if os.name == 'nt' else '/'
            total, used, free = shutil.disk_usage(drive)
            
            usage_info['total'] = format_size(total)
            usage_info['used'] = format_size(used)
            usage_info['free'] = format_size(free)
            if total > 0:
                percent = (used / total) * 100
                usage_info['percent'] = f"{percent:.1f}%"
            else:
                usage_info['percent'] = "0%"
        except Exception as e:
            logger.error(f"Error getting disk usage: {e}")
            usage_info['error'] = str(e)
        return usage_info

    def find_duplicates(self, start_path):
        """Finds duplicate files based on size and content hash."""
        duplicates = []
        size_map = defaultdict(list)
        
        if not os.path.exists(start_path):
            return duplicates

        # 1. Group by size
        try:
            for root, _, files in os.walk(start_path):
                for name in files:
                    filepath = os.path.join(root, name)
                    try:
                        if os.path.islink(filepath):
                            continue
                        size = os.path.getsize(filepath)
                        if size > 0:
                            size_map[size].append(filepath)
                    except OSError:
                        pass
        except Exception:
            pass

        # 2. Check hash for files with same size
        for size, paths in size_map.items():
            if len(paths) > 1:
                hash_map = defaultdict(list)
                for path in paths:
                    try:
                        with open(path, 'rb') as f:
                            # Read first 64kb for speed optimization
                            chunk = f.read(65536)
                            file_hash = hashlib.md5(chunk).hexdigest()
                            hash_map[file_hash].append(path)
                    except OSError:
                        pass
                
                for file_hash, same_hash_paths in hash_map.items():
                    if len(same_hash_paths) > 1:
                        duplicates.append((size, same_hash_paths))

        return duplicates

    def find_large_files(self, start_path, min_size_mb=100):
        """Finds files larger than a specific size (default 100MB)."""
        large_files = []
        min_size_bytes = min_size_mb * 1024 * 1024
        
        if not os.path.exists(start_path):
            return large_files

        try:
            for root, _, files in os.walk(start_path):
                for name in files:
                    try:
                        filepath = os.path.join(root, name)
                        # Skip symlinks to avoid infinite loops or wrong sizes
                        if os.path.islink(filepath):
                            continue
                            
                        size = os.path.getsize(filepath)
                        if size > min_size_bytes:
                            large_files.append((filepath, format_size(size)))
                    except OSError:
                        pass
        except Exception as e:
            logger.error(f"Error scanning for large files in {start_path}: {e}")
            
        return large_files

    def generate_report(self):
        """Generates a text report of system health."""
        report = []
        report.append("=== SYSTEM HEALTH REPORT ===")
        
        # Metrics
        metrics = self.get_system_metrics()
        report.append("\n[System Metrics]")
        for k, v in metrics.items():
            report.append(f"{k.replace('_', ' ').title()}: {v}")
            
        # Disk Usage
        disk = self.get_disk_usage()
        report.append("\n[Disk Usage (Main Drive)]")
        for k, v in disk.items():
            report.append(f"{k.title()}: {v}")
            
        # Large Files (Example: Scan User Profile Documents/Downloads if on Windows)
        # Scanning the whole drive might be too slow for a quick report, so let's stick to Downloads for now as a demo.
        report.append("\n[Large Files (>100MB) in Downloads]")
        target_dir = ''
        if os.name == 'nt':
            target_dir = os.path.join(os.environ.get('USERPROFILE', ''), 'Downloads')
        else:
            target_dir = '/tmp' # Just for testing context
            
        large_files = self.find_large_files(target_dir)
        if large_files:
            for path, size in large_files:
                report.append(f"{size} - {path}")
        else:
            report.append("No large files found or directory skipped.")
        
        # Duplicates (Same target directory for demo)
        report.append("\n[Duplicate Files in Downloads]")
        duplicates = self.find_duplicates(target_dir)
        if duplicates:
            for size, paths in duplicates:
                report.append(f"Size: {format_size(size)}")
                for p in paths:
                    report.append(f"  - {p}")
        else:
            report.append("No duplicate files found.")

        return "\n".join(report)
