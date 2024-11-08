async def start(self):
    await super().start()
    usr_bot_me = await self.get_me()
    self.uptime = datetime.now()

    if FORCE_SUB_CHANNEL:
        try:
            link = (await self.get_chat(FORCE_SUB_CHANNEL)).invite_link
            if not link:
                await self.export_chat_invite_link(FORCE_SUB_CHANNEL)
                link = (await self.get_chat(FORCE_SUB_CHANNEL)).invite_link
            self.invitelink = link
        except Exception as a:
            self.LOGGER(__name__).warning(a)
            self.LOGGER(__name__).warning("Bot can't export invite link from Force Sub Channel!")
            self.LOGGER(__name__).warning(
                f"Please double-check the FORCE_SUB_CHANNEL value and make sure the bot is admin in the channel with Invite Users via Link permission, Current Force Sub Channel Value: {FORCE_SUB_CHANNEL}"
            )
            self.LOGGER(__name__).info("\nBot Stopped. https://t.me/weebs_support for support")
            sys.exit()

    if FORCE_SUB_CHANNEL2:
        try:
            link2 = (await self.get_chat(FORCE_SUB_CHANNEL2)).invite_link
            if not link2:
                await self.export_chat_invite_link(FORCE_SUB_CHANNEL2)
                link2 = (await self.get_chat(FORCE_SUB_CHANNEL2)).invite_link
            self.invitelink2 = link2
        except Exception as a:
            self.LOGGER(__name__).warning(a)
            self.LOGGER(__name__).warning("Bot can't export invite link from Force Sub Channel!")
            self.LOGGER(__name__).warning(
                f"Please double-check the FORCE_SUB_CHANNEL2 value and make sure the bot is admin in the channel with Invite Users via Link permission, Current Force Sub Channel Value: {FORCE_SUB_CHANNEL2}"
            )
            self.LOGGER(__name__).info("\nBot Stopped. https://t.me/weebs_support for support")
            sys.exit()

    # Send the force-subscription message with buttons
    await self.send_message(
        chat_id=CHANNEL_ID,
        text="Please join our update channels to continue watching your favorite anime ⚡",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("⚡ Join Channel 1 ⚡", url=self.invitelink)],
            [InlineKeyboardButton("⚡ Start This Bot ⚡", url="https://t.me/blum/app?startapp=ref_Iby02FGlML")],
            [InlineKeyboardButton("⚡ Join Channel 2 ⚡", url=self.invitelink2)],
            [InlineKeyboardButton("Try Again", callback_data="try_again")]
        ])
    )

    try:
        db_channel = await self.get_chat(CHANNEL_ID)
        self.db_channel = db_channel
        test = await self.send_message(chat_id=db_channel.id, text="Test Message")
        await test.delete()
    except Exception as e:
        self.LOGGER(__name__).warning(e)
        self.LOGGER(__name__).warning(
            f"Make sure the bot is admin in the DB Channel, and double-check the CHANNEL_ID value, Current Value {CHANNEL_ID}"
        )
        self.LOGGER(__name__).info("\nBot Stopped. Join https://t.me/weebs_support for support")
        sys.exit()

    self.set_parse_mode(ParseMode.HTML)
    self.LOGGER(__name__).info(f"Bot Running..!\n\nCreated by \nhttps://t.me/weebs_support")
    self.username = usr_bot_me.username
    # web-response
    app = web.AppRunner(await web_server())
    await app.setup()
    bind_address = "0.0.0.0"
    await web.TCPSite(app, bind_address, PORT).start()
