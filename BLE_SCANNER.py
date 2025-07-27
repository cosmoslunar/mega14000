import asyncio
from bleak import BleakScanner

def estimate_distance(rssi, tx_power=-59):
    if rssi == 0:
        return None
    ratio = rssi / tx_power
    if ratio < 1.0:
        return round(pow(ratio, 10), 2)
    else:
        return round(0.89976 * pow(ratio, 7.7095) + 0.111, 2)

async def scan_ble_devices():
    print("=" * 40)
    print("BLE SCANNER".center(40))
    print("=" * 40)
    print("스캔 중... (5초간)\n")
    devices = await BleakScanner.discover(timeout=5.0)

    if not devices:
        print("BLE 장치 없음.\n")
    else:
        for d in devices:
            print("-" * 40)
            print(f"이름: {d.name or '알 수 없음'}")
            print(f"MAC: {d.address}")
            print(f"RSSI: {d.rssi} dBm")
            distance = estimate_distance(d.rssi)
            print(f"추정 거리: 약 {distance} m" if distance else "거리 추정 불가")
            if d.metadata and "uuids" in d.metadata:
                print("UUIDs:")
                for uuid in d.metadata["uuids"]:
                    print(f"  - {uuid}")
            else:
                print("UUID 정보 없음.")
        print("-" * 40 + "\n")

async def main():
    while True:
        await scan_ble_devices()
        cmd = input("다시 스캔하려면 Enter 키를 누르세요, 종료하려면 q 입력 > ").strip().lower()
        if cmd == "q":
            print("종료합니다.")
            break

asyncio.run(main())