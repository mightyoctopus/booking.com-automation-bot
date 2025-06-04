from booking.booking import Booking
import booking.constants as const

# inst = Booking()
# inst.land_first_page()

with Booking() as bot:
    bot.land_first_page()
    bot.set_currency(currency="U.S. Dollar")
    bot.select_destination(destination="haneda")
    bot.select_dates(check_in_date="2025-06-03", check_out_date="2025-06-05")
    bot.press_company_members_bar()
    bot.select_adults(num_of_adults=2)
    bot.select_rooms(num_of_rooms=1)
    bot.hit_search_btn()

    bot.apply_filtering()
    bot.refresh() # a workaround to let the bot grab the data properly.
    bot.report_results()




# Javascript code on the browser console
# const hotelName = document.querySelectorAll('[data-testid="title"]');
