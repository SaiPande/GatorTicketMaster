# GatorTicketMaster

## Project Overview

The Gator Ticket Master is a seating booking system designed to maximize seat allocation and reservation for Gator Events. It uses advanced data structures such as Red-Black Tree and Min Heap to efficiently manage seat reservations, cancellations, and waitlist operations.

## Key Features
- Seat Reservations
- Cancellations
- Waitlist Management
- Dynamic Seat Additions
- Efficient performance with O(log n) time complexity
- Data Structures Used


## Red-Black Tree
- A self-balancing binary search tree used to store reserved seat information.
- Each node has a user ID (key) and seat ID.
- Time Complexity: Insertion, Deletion, and Search → O(log n)

## Min Heap
- A priority queue to manage the waitlist.
- Prioritizes users based on priority and timestamp.
- Time Complexity: Insert, Delete Minimum → O(log n), Get Minimum → O(1)

## Project Structure
- Node: Represents a node in the Red-Black Tree.
- RedBlackTree: Implements the Red-Black Tree data structure.
- MinHeap: Uses Min Heap for queue management.
- GatorTicketMaster: Main class that includes all core functionalities.

## Programming Environment
Language: Python 3
Interface: Command Line Interface (CLI)

## How to Run the Program

Command Line Execution:

```bash
$ python3 gatorTicketMaster.py <input_filename>
```
Example:
```bash
$ python3 gatorTicketMaster.py input.txt
```

Output: <input_filename>_output_file.txt

Using Makefile:

```bash
$ make run INPUT_FILE=input.txt
```

## Main Functions

### GatorTicketMaster Class

initialize(seat_count): Initializes the ticket system with a given number of seats.

available(): Returns the number of available seats and waitlist size.

reserve(user_id, user_priority): Reserves a seat or adds the user to the waitlist.

cancel(seat_id, user_id): Cancels a reservation and reassigns the seat.

add_seats(count): Adds new seats and processes the waitlist.

print_reservations(): Displays all reservations sorted by seat ID.

exit_waitlist(user_id): Removes a user from the waitlist.

update_priority(user_id, user_priority): Updates a user's priority in the waitlist.

release_seats(user_id1, user_id2): Releases seats for users within the given ID range.

### RedBlackTree Class

insert(user_id, seat_id): Inserts a node into the tree.

delete(user_id): Deletes a node from the tree.

search(user_id): Searches for a node with the given user ID.

### MinHeap Class

insert(priority, user_id): Inserts a user into the heap.

extract_min(): Removes and returns the user with the highest priority.

remove(user_id): Removes a user from the heap.

update_priority(user_id, new_priority): Updates a user's priority.

## Example Input/Output

**Input File: input.txt**

Initialize 5
Reserve 101 1
Reserve 102 2
Cancel 1 101
AddSeats 3
PrintReservations
Quit

**Output File: input_output_file.txt**

Initialization complete: 5 seats available
Seat reserved: User 101 - Seat 1
Seat reserved: User 102 - Seat 2
Reservation canceled: Seat 1 - User 101
Seats added: 3
Reservations: Seat 2 - User 102


## Performance

Red-Black Tree: Efficient for seat lookups and updates with O(log n) complexity.

Min Heap: Fast waitlist management with O(1) access to the highest-priority user.

Scalability: Suitable for both small and large events.

## Conclusion

The Gator Ticket Master system efficiently handles seat reservations, cancellations, and waitlists using advanced data structures. It ensures that the highest-priority users are served first while maintaining quick lookups and updates, making it perfect for managing both small and large-scale events.

## Author

Name: Sai Pande
University: University of Florida, Computer Science and Information Science Engineering
Email: saipande@ufl.edu