#!/usr/bin/env python3
"""
NetVision - Lightweight Network Security Monitor
Main CLI module: netvision.py
Created by 6lackRaven
"""

import argparse
import logging
import sys
import signal
import subprocess
import os
import json
import threading
import queue
import time
from pathlib import Path
from utils.format import colorize, Color
from core import detect, logger as alert_logger

# Global configuration
APP_NAME = "NetVision"
VERSION = "1.0"
BANNER = f"""
{colorize('▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓', Color.BLUE)}
▓                                                            ▓
▓  {colorize('███╗   ██╗███████╗████████╗██╗   ██╗██╗███████╗██╗ ██████╗ ███╗   ██╗', Color.CYAN)}  ▓
▓  {colorize('████╗  ██║██╔════╝╚══██╔══╝██║   ██║██║██╔════╝██║██╔═══██╗████╗  ██║', Color.CYAN)}  ▓
▓  {colorize('██╔██╗ ██║█████╗     ██║   ██║   ██║██║███████╗██║██║   ██║██╔██╗ ██║', Color.CYAN)}  ▓
▓  {colorize('██║╚██╗██║██╔══╝     ██║   ╚██╗ ██╔╝██║╚════██║██║██║   ██║██║╚██╗██║', Color.CYAN)}  ▓
▓  {colorize('██║ ╚████║███████╗   ██║    ╚████╔╝ ██║███████║██║╚██████╔╝██║ ╚████║', Color.CYAN)}  ▓
▓  {colorize('╚═╝  ╚═══╝╚══════╝   ╚═╝     ╚═══╝  ╚═╝╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝', Color.CYAN)}  ▓
▓                                                            ▓
▓  {colorize('»»——⧋ Real-time Network Threat Detection ⧋——««', Color.MAGENTA)}  ▓
▓  {colorize('»»——⧋ Created by 6lackRaven ⧋——««', Color.YELLOW)}  ▓
▓                                                            ▓
{colorize('▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓', Color.BLUE)}
"""

def setup_logging(verbose=False):
    """Configure logging system"""
    log_level = logging.DEBUG if verbose else logging.INFO
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    logging.basicConfig(
        level=log_level,
        format=log_format,
        handlers=[
            logging.FileHandler("netvision_debug.log"),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(APP_NAME)

def signal_handler(sig, frame):
    """Handle CTRL-C interruption"""
    log.info(colorize("\n🛑 Shutdown signal received. Stopping sniffing...", Color.YELLOW))
    stop_sniffer()
    sys.exit(0)

def compile_c_sniffer():
    """Compile the C-based sniffer executable"""
    sniffer_dir = Path("sniffer")
    sniffer_src = sniffer_dir / "sniffer.c"
    sniffer_bin = sniffer_dir / "sniffer"
    
    if not sniffer_src.exists():
        log.error(f"Sniffer source not found at {sniffer_src}")
        return None
        
    if sniffer_bin.exists():
        # Check if binary is newer than source
        src_mtime = os.path.getmtime(sniffer_src)
        bin_mtime = os.path.getmtime(sniffer_bin)
        if bin_mtime > src_mtime:
            return sniffer_bin
    
    log.info("🔨 Compiling C sniffer for high-performance packet capture...")
    compile_cmd = f"gcc -O3 -o {sniffer_bin} {sniffer_src} -lpcap"
    result = subprocess.run(
        compile_cmd, 
        shell=True, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE
    )
    
    if result.returncode != 0:
        log.error(f"❌ Compilation failed:\n{result.stderr.decode()}")
        return None
        
    log.info(f"✅ Sniffer compiled to {sniffer_bin}")
    return sniffer_bin

def start_sniffer(interface=None, pkt_queue=None):
    """Start C-based sniffer as subprocess"""
    sniffer_bin = compile_c_sniffer()
    if not sniffer_bin:
        log.critical("Failed to compile sniffer. Exiting.")
        sys.exit(1)
    
    cmd = [str(sniffer_bin)]
    if interface:
        cmd.extend(["-i", interface])
    
    log.info(f"📡 Starting C sniffer on {interface or 'default interface'}")
    
    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # Start stderr reader thread
        def read_stderr():
            while True:
                line = process.stderr.readline()
                if not line:
                    break
                log.error(f"SNIFFER: {line.strip()}")
        
        stderr_thread = threading.Thread(target=read_stderr, daemon=True)
        stderr_thread.start()
        
        # Start stdout reader thread
        def read_stdout():
            while True:
                line = process.stdout.readline()
                if not line:
                    break
                try:
                    pkt_data = json.loads(line.strip())
                    pkt_queue.put(pkt_data)
                except json.JSONDecodeError:
                    log.warning(f"Invalid JSON from sniffer: {line}")
        
        stdout_thread = threading.Thread(target=read_stdout, daemon=True)
        stdout_thread.start()
        
        return process
        
    except Exception as e:
        log.critical(f"Failed to start sniffer: {str(e)}")
        return None

def stop_sniffer(process=None):
    """Stop the sniffer subprocess"""
    if process and process.poll() is None:
        process.terminate()
        try:
            process.wait(timeout=3.0)
            log.info("✋ Sniffer stopped cleanly")
        except subprocess.TimeoutExpired:
            process.kill()
            log.warning("⚠️ Sniffer forcefully killed")

def process_packet(pkt_data):
    """Process packet through detection pipeline"""
    try:
        # Skip packets without IP data
        if not pkt_data.get('src_ip') or not pkt_data.get('protocol'):
            return
            
        # Analyze for security threats
        alerts = detect.analyze_packet(pkt_data)
        
        # Log any detected alerts
        for alert in alerts:
            alert_logger.log_alert(alert, pkt_data)
            
    except Exception as e:
        log.error(f"Packet processing error: {str(e)}")

def packet_processor(pkt_queue):
    """Process packets from queue"""
    log.info("🚀 Starting packet processing engine")
    while True:
        try:
            pkt_data = pkt_queue.get(timeout=1.0)
            if pkt_data is None:  # Sentinel value for shutdown
                break
            process_packet(pkt_data)
        except queue.Empty:
            continue
        except Exception as e:
            log.error(f"Processor error: {str(e)}")
    log.info("🛑 Packet processor stopped")

def parse_arguments():
    """Parse command-line arguments with detailed help"""
    parser = argparse.ArgumentParser(
        description=f"{APP_NAME} - Network Monitoring and Threat Detection",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    # Interface options
    parser.add_argument(
        '-i', '--interface',
        default=None,
        help='Network interface to monitor (e.g. eth0, wlan0)'
    )
    
    # Verbosity options
    parser.add_argument(
        '-v', '--verbose',
        action='count',
        default=0,
        help='Increase verbosity level (-v: INFO, -vv: DEBUG)'
    )
    
    # Capture duration
    parser.add_argument(
        '-t', '--timeout',
        type=int,
        default=0,
        help='Capture duration in seconds (0 = run until interrupted)'
    )
    
    # Logging options
    parser.add_argument(
        '-l', '--logfile',
        default="netvision.log",
        help='Path to save alert logs'
    )
    
    # Output format
    parser.add_argument(
        '-f', '--format',
        choices=['text', 'json'],
        default='text',
        help='Output format for alerts'
    )
    
    return parser.parse_args()

if __name__ == '__main__':
    print(BANNER)
    args = parse_arguments()
    
    # Configure logging based on verbosity
    if args.verbose == 0:
        log_level = logging.WARNING
    elif args.verbose == 1:
        log_level = logging.INFO
    else:
        log_level = logging.DEBUG
    
    log = setup_logging(log_level == logging.DEBUG)
    log.setLevel(log_level)
    
    # Configure alert logger
    alert_logger.LOG_PATH = args.logfile
    
    # Register signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    
    # Create packet queue and processor thread
    pkt_queue = queue.Queue()
    processor_thread = threading.Thread(
        target=packet_processor, 
        args=(pkt_queue,),
        daemon=True
    )
    processor_thread.start()
    
    # Start sniffer subprocess
    sniffer_proc = start_sniffer(args.interface, pkt_queue)
    if not sniffer_proc:
        log.critical("❌ Failed to start packet capture")
        sys.exit(1)
    
    try:
        start_time = time.time()
        log.info(colorize(f"🚀 Started NetVision at {time.ctime(start_time)}", Color.GREEN))
        
        # Monitor sniffer status
        while sniffer_proc.poll() is None:
            # Handle timeout if specified
            if args.timeout > 0 and (time.time() - start_time) > args.timeout:
                log.info("⏰ Capture timeout reached")
                break
                
            time.sleep(0.5)
            
    except Exception as e:
        log.critical(colorize(f"💥 Critical failure: {str(e)}", Color.RED))
    finally:
        # Cleanup resources
        stop_sniffer(sniffer_proc)
        pkt_queue.put(None)  # Signal processor to stop
        processor_thread.join(timeout=2.0)
        
        log.info(colorize(f"🛑 NetVision shutdown at {time.ctime()}", Color.YELLOW))
        log.info(f"📊 Alerts saved to {args.logfile}")
        print("\n" + colorize("➤ Monitoring stopped. Stay secure!", Color.CYAN))
