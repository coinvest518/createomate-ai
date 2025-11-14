#!/usr/bin/env python3
"""
Railway Entry Point - FDWA Automated Marketing System
"""
import os
import sys
from fdwa_auto_marketing import FDWAAutoMarketing

def main():
    """Main entry point for Railway deployment"""
    print("🚀 Starting FDWA Automated Marketing System on Railway...")
    
    # Initialize and start the marketing automation
    auto_marketing = FDWAAutoMarketing()
    auto_marketing.start_scheduler()

if __name__ == "__main__":
    main()