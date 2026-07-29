import asyncio
import sys
from pyrogram import idle
from Chizuru import Chizuru, userbot, pytgcalls

async def main():
    print("""
╔══════════════════════════════════════════════════════╗
║              🎵 Chizuru Music Bot 🎵                ║
║         Telegram Voice Chat Music Player             ║
╚══════════════════════════════════════════════════════╝
    """)
    
    try:
        await userbot.start()
        print("🤖 Assistant Started!")
        
        await Chizuru.start()
        print("🤖 Bot Started!")
        
        await pytgcalls.start()
        print("🎵 PyTgCalls Started!")
        
        print("\n✅ All systems ready!")
        print("📌 Commands: /play, /vplay, /skip, /pause, /resume, /stop")
        print("="*50)
        
        await idle()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
