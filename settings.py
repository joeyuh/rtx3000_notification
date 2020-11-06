class Settings:   # The Settings class

    # Timing
    BETWEEN_ROUNDS = 4
    TIMEOUT = 3.0
    TIMEOUT_RETRY = 4.0
    UNKNOWN_ERROR_RETRY = 2.0
    MAX_RETRIES = 3
    BOT_RETRY = 10

    # Notification
    AUDIO_ALERT = True
    beep_time = 30

    OPEN_IN_BROWSER = True

    EMAIL_ALERT = True
    sender_email_address = 'gooddealscript@gmail.com'  # Gmail only
    sender_email_password = 'whataPassword'
    recipients = ['grandpajoe278@gmail.com']
    subject = 'IN STOCK ALERT '

    SMS = False  # In development, not free service, probably not gonna deploy

    # URL
    bestbuty_url_bank = [
        "https://www.bestbuy.com/site/nvidia-geforce-rtx-3070-8gb-gddr6-pci-express-4-0-graphics-card-dark-platinum-and-black/6429442.p?skuId=6429442",
        "https://www.bestbuy.com/site/nvidia-geforce-rtx-3080-10gb-gddr6x-pci-express-4-0-graphics-card-titanium-and-black/6429440.p?skuId=6429440",
        # "https://www.bestbuy.com/site/nvidia-geforce-rtx-3090-24gb-gddr6x-pci-express-4-0-graphics-card-titanium-and-black/6429434.p?skuId=6429434",
        "https://www.bestbuy.com/site/evga-geforce-rtx-3070-xc3-black-gaming-8gb-gddr6x-pci-express-4-0-graphics-card/6439300.p?skuId=6439300",
        "https://www.bestbuy.com/site/gigabyte-geforce-rtx-3080-10g-gddr6x-pci-express-4-0-graphics-card-black/6430620.p?skuId=6430620",
        "https://www.bestbuy.com/site/pny-geforce-rtx-3080-10gb-xlr8-gaming-epic-x-rgb-triple-fan-graphics-card/6432655.p?skuId=6432655",
        "https://www.bestbuy.com/site/evga-geforce-rtx-3080-ftw3-gaming-10gb-gddr6x-pci-express-4-0-graphics-card/6436191.p?skuId=6436191",
        "https://www.bestbuy.com/site/gigabyte-geforce-rtx-3080-10g-gddr6x-pci-express-4-0-graphics-card-white/6436219.p?skuId=6436219",
        "https://www.bestbuy.com/site/pny-geforce-rtx-3070-8gb-dual-fan-graphics-card/6432654.p?skuId=6432654",
        "https://www.bestbuy.com/site/evga-geforce-rtx-3080-xc3-black-gaming-10gb-gddr6x-pci-express-4-0-graphics-card/6432399.p?skuId=6432399",
        # "https://www.bestbuy.com/site/asus-geforce-rtx-3090-24gb-gddr6x-pci-express-4-0-strix-graphics-card-black/6432447.p?skuId=6432447",
        "https://www.bestbuy.com/site/msi-geforce-rtx-3080-ventus-3x-10g-oc-bv-gddr6x-pci-express-4-0-graphic-card-black-silver/6430175.p?skuId=6430175",
        "https://www.bestbuy.com/site/gigabyte-geforce-rtx-3070-8g-gddr6-pci-express-4-0-graphics-card-black/6437909.p?skuId=6437909",
        "https://www.bestbuy.com/site/evga-geforce-rtx-3080-xc3-ultra-gaming-10gb-gddr6x-pci-express-4-0-graphics-card/6432400.p?skuId=6432400",
        # "https://www.bestbuy.com/site/evga-geforce-rtx-3090-ftw3-gaming-24gb-gddr6x-pci-express-4-0-graphics-card/6436193.p?skuId=6436193",
        "https://www.bestbuy.com/site/gigabyte-geforce-rtx-3080-10g-gddr6x-pci-express-4-0-graphics-card-black/6430621.p?skuId=6430621",
        # "https://www.bestbuy.com/site/evga-geforce-rtx-3090-ftw3-ultra-gaming-24gb-gddr6x-pci-express-4-0-graphics-card/6436192.p?skuId=6436192",
        "https://www.bestbuy.com/site/evga-geforce-rtx-3080-xc3-ultra-gaming-10gb-gddr6x-pci-express-4-0-graphics-card/6436195.p?skuId=6436195",
        "https://www.bestbuy.com/site/evga-geforce-rtx-3080-xc3-gaming-10gb-gddr6x-pci-express-4-0-graphics-card/6436194.p?skuId=6436194",
        "https://www.bestbuy.com/site/pny-geforce-rtx-3080-10gb-xlr8-gaming-epic-x-rgb-triple-fan-graphics-card/6432658.p?skuId=6432658",
        # "https://www.bestbuy.com/site/asus-tuf-rtx-3090-24gb-gddr6x-pci-express-4-0-graphics-card-black/6432446.p?skuId=6432446",
        # "https://www.bestbuy.com/site/evga-geforce-rtx-3090-xc3-gaming-24gb-gddr6x-pci-express-4-0-graphics-card/6434363.p?skuId=6434363",
        "https://www.bestbuy.com/site/gigabyte-geforce-rtx-3090-24g-gddr6x-pci-express-4-0-graphics-card-black/6430623.p?skuId=6430623",
        # "https://www.bestbuy.com/site/gigabyte-geforce-rtx-3090-24g-gddr6x-pci-express-4-0-graphics-card-black/6437910.p?skuId=6437910",
        # "https://www.bestbuy.com/site/pny-geforce-rtx-3090-24gb-xlr8-gaming-epic-x-rgb-triple-fan-graphics-card/6432656.p?skuId=6432656",
        # "https://www.bestbuy.com/site/msi-geforce-rtx-3090-ventus-3x-24g-oc-bv-24gb-gddr6x-pci-express-4-0-graphics-card-black-silver/6430215.p?skuId=6430215",
        # "https://www.bestbuy.com/site/gigabyte-geforce-rtx-3090-24g-gddr6x-pci-express-4-0-graphics-card-black/6430624.p?skuId=6430624",
        # "https://www.bestbuy.com/site/pny-geforce-rtx-3090-24gb-xlr8-gaming-epic-x-rgb-triple-fan-graphics-card/6432657.p?skuId=6432657",
        # "https://www.bestbuy.com/site/msi-nvidia-geforce-gtx-1650-super-4gb-gddr6-pci-express-3-0-graphics-card-black-gray/6397798.p?skuId=6397798",
        # Debugging if Yes works, the last one should always be in stock

        # AMD Ryzen 5000
        "https://www.bestbuy.com/site/amd-ryzen-5-5600x-4th-gen-6-core-12-threads-unlocked-desktop-processor-with-wraith-stealth-cooler/6438943.p?skuId=6438943",
        "https://www.bestbuy.com/site/amd-ryzen-7-5800x-4th-gen-8-core-16-threads-unlocked-desktop-processor-without-cooler/6439000.p?skuId=6439000",
        "https://www.bestbuy.com/site/amd-ryzen-9-5900x-4th-gen-12-core-24-threads-unlocked-desktop-processor-without-cooler/6438942.p?skuId=6438942",
        "https://www.bestbuy.com/site/amd-ryzen-9-5950x-4th-gen-16-core-32-threads-unlocked-desktop-processor-without-cooler/6438941.p?skuId=6438941"
    ]

    # RTX 3070 and RTX 3080 only
    amazon_url_bank = [
        "https://www.amazon.com/ZOTAC-Graphics-IceStorm-Advanced-ZT-A30800D-10P/dp/B08HJNKT3P?ref_=ast_sto_dp&th=1&psc=1",
        "https://www.amazon.com/ASUS-Graphics-DisplayPort-Military-Grade-Certification/dp/B08HH5WF97?ref_=ast_sto_dp",
        "https://www.amazon.com/ASUS-Graphics-DisplayPort-Military-Grade-Certification/dp/B08HHDP9DW?ref_=ast_sto_dp",
        "https://www.amazon.com/PNY-GeForce-Gaming-Epic-X-Graphics/dp/B08HBR7QBM?ref_=ast_sto_dp&th=1&psc=1",
        "https://www.amazon.com/PNY-GeForce-Gaming-Uprising-Graphics/dp/B08HBTJMLJ?ref_=ast_sto_dp&th=1&psc=1",
        "https://www.amazon.com/MSI-GeForce-RTX-3080-10G/dp/B08HR5SXPS?ref_=ast_sto_dp",
        "https://www.amazon.com/MSI-GeForce-RTX-3080-10G/dp/B08HR7SV3M?ref_=ast_sto_dp",
        "https://www.amazon.com/EVGA-10G-P5-3897-KR-GeForce-Technology-Backplate/dp/B08HR3Y5GQ?ref_=ast_sto_dp",
        "https://www.amazon.com/EVGA-10G-P5-3895-KR-GeForce-Technology-Backplate/dp/B08HR3DPGW?ref_=ast_sto_dp",
        "https://www.amazon.com/EVGA-10G-P5-3885-KR-GeForce-Cooling-Backplate/dp/B08HR55YB5?ref_=ast_sto_dp",
        "https://www.amazon.com/EVGA-10G-P5-3883-KR-GeForce-Cooling-Backplate/dp/B08HR4RJ3Q?ref_=ast_sto_dp",
        "https://www.amazon.com/EVGA-10G-P5-3881-KR-GeForce-GAMING-Cooling/dp/B08HR6FMF3?ref_=ast_sto_dp",
        "https://www.amazon.com/GIGABYTE-Graphics-WINDFORCE-GV-N3080GAMING-OC-10GD/dp/B08HJTH61J?ref_=ast_sto_dp&th=1&psc=1",
        "https://www.amazon.com/Gigabyte-Graphics-WINDFORCE-GV-N3080EAGLE-OC-10GD/dp/B08HJS2JLJ?ref_=ast_sto_dp",
        "https://www.amazon.com/dp/B08HBF5L3K/ref=twister_B08M7B1ZK7?_encoding=UTF8&th=1",
        "https://www.amazon.com/EVGA-08G-P5-3751-KR-GeForce-Gaming-Cooling/dp/B08LW46GH2",
        "https://www.amazon.com/ZOTAC-Graphics-IceStorm-Advanced-ZT-A30700H-10P/dp/B08LF1CWT2",
        "https://www.amazon.com/ASUS-Graphics-DisplayPort-Axial-tech-2-9-Slot/dp/B08L8JNTXQ",
        "https://www.amazon.com/MSI-GeForce-256-Bit-Architecture-Graphics/dp/B08KWLMZV4",
        # 'https://www.amazon.com/Skytech-Prism-Gaming-Desktop-Motherboard/dp/B08K1C22YY'
        # Debugging if Yes works, the last one should always be in stock

    ]

    html_template = '''
    <!DOCTYPE html>
    <html>
    <body>
    <h1 style="text-align: center;"><strong><a href="{0}">CLICK HERE</a></strong></h1>
    </br>
    {0}
    </body>
    </html>
        '''