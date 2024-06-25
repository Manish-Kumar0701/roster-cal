from django.shortcuts import render
from .forms import SeatAllocationForm

# Define your vertical and horizontal reservation percentages
vertical_reservation = {
    "Bhutia and Lepcha 20%": 20,
    "OBC - Central List 20%": 20,
    "OBC - State List 20%": 20,
    "Scheduled Tribes 13%": 13,
    "Scheduled Castes 6%": 6,
    "Primitive Tribe 5%": 5,
    "Most Backward Classes - State List 3%": 3,
    "Weaker Sections of the Society 2%": 2,
}

horizontal_reservation = {
    "Women": 33,
    "Sports Persons and Artisans of Excellence": 5,
    "Below Poverty Line families": 5,
    "Ex-Servicemen": 3,
    "Paramilitary forces and Assam Rifles": 2,
    "Persons with Disabilities": {
        "Blind and Low Vision": 1,
        "Deaf and Hard of Hearing": 1,
        "Locomotor Disability": 1,
        "Mental Illness & Multiple Disabilities": 1,
    }
}

def custom_round(value):
    if value - int(value) < 0.5:
        return int(value)
    else:
        return int(value) + 1

def calculate_vertical_seats(total_seats, vertical_reservation):
    allocated_seats = 0
    vertical_seats = {}
    
    for category, percentage in vertical_reservation.items():

        seats = custom_round(total_seats * percentage / 100)
   
        vertical_seats[category] = seats
        allocated_seats += seats
    
    general_seats = total_seats - allocated_seats
    vertical_seats[category] = seats
    return vertical_seats, general_seats

def distribute_horizontal_seats(vertical_seats, horizontal_reservation, total_seats):
    allocation = {category: {} for category in vertical_seats}
    total_allocated_seats = {category: 0 for category in vertical_seats}
  
    for category, seats in horizontal_reservation.items():
        if isinstance(seats, int):
            for vert_category in vertical_seats:
                allocated_seats = custom_round((seats / 100) * vertical_seats[vert_category])
                allocation[vert_category][category] = allocated_seats
                vertical_seats[vert_category] -= allocated_seats
                total_allocated_seats[vert_category] += allocated_seats
        else:
            for sub_category, sub_seats in seats.items():
                for vert_category in vertical_seats:
                    allocated_seats = custom_round((sub_seats / 100) * vertical_seats[vert_category])
                    allocation[vert_category][sub_category] = allocated_seats
                    vertical_seats[vert_category] -= allocated_seats
                    total_allocated_seats[vert_category] += allocated_seats

    for vert_category in vertical_seats:
        remaining_seats = vertical_seats[vert_category]
        allocation[vert_category]["generalSeat"] = remaining_seats
        total_allocated_seats[vert_category] += remaining_seats

    return allocation

def allocate_seats(request):
    if request.method == "POST":
        form = SeatAllocationForm(request.POST)
        if form.is_valid():
            total_seats = form.cleaned_data['total_seats']
            vertical_seats, general_seats = calculate_vertical_seats(total_seats, vertical_reservation)
            values = vertical_seats
            print(' first old_vertical_seats',values)
        
            allocation = distribute_horizontal_seats(vertical_seats, horizontal_reservation, total_seats)
            print('form',form)
            print('total_seats',total_seats)
            print('old_vertical_seats',values,'general_seats',general_seats,'allocation',allocation)
            return render(request, 'allocation/results.html', {
                'form': form,
                'total_seats': total_seats,
                'vertical_seats': vertical_seats,
                'general_seats': general_seats,
                'allocation': allocation,
            })
    else:
        form = SeatAllocationForm()
    
    return render(request, 'allocation/form.html', {'form': form})
