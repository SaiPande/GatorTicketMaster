from datetime import datetime
import sys

#This is a Node class for the Red-Black Tree. It represents a reservation with user_id, seat_id, color, and pointers to left child, right child, and parent nodes
class Node:
    def __init__(self, user_id: int, seat_id: int):
        self.user_id = user_id
        self.seat_id = seat_id
        self.color = 1  # 1 is for color red and 0 is for color black
        self.left = None
        self.right = None
        self.parent = None

class RedBlackTree:
    #The RedBlackTree class is initialized with an empty node and this node is sets as the root
    def __init__(self):
        self.NIL = Node(0, 0) 
        self.NIL.color = 0  #0 = black, 1 = red
        self.root = self.NIL #we assign the node black color

    #search() searches for a node with the given user_id.
    def search(self, user_id: int):
        def _search_helper(node, user_id):
            if node == self.NIL or user_id == node.user_id:   #if the first node is the required node, we return it
                return node
            
            #if the required node is less than the current node, we recursively move to left in search of the node(recursion is implemented in search helper function)
            if user_id < node.user_id:
                return _search_helper(node.left, user_id)
            
            #if the required node is greater than the current node, we recursively move to right in search of the node(recursion is implemented in search helper function)
            return _search_helper(node.right, user_id)
        return _search_helper(self.root, user_id)    

    #In the inserts(), a new node into the Red-Black Tree, maintaining its properties
    def insert(self, user_id: int, seat_id: int):
        node = Node(user_id, seat_id)  #create the new node to be inserted
        node.left = self.NIL
        node.right = self.NIL
        trail_pntr = None
        trav_pntr = self.root

        #using binary search tree insertion, we traverse from root to left or right till we find new node's appropriate position in the tree
        while trav_pntr != self.NIL:
            trail_pntr = trav_pntr
            if node.user_id < trav_pntr.user_id:
                trav_pntr = trav_pntr.left
            else:
                trav_pntr = trav_pntr.right

        node.parent = trail_pntr

        if trail_pntr is None:
            self.root = node
        elif node.user_id < trail_pntr.user_id:
            trail_pntr.left = node
        else:
            trail_pntr.right = node

        node.color = 1
        self._correct_insert_node(node)  #we call correct insert node function to maintain the redblack tree properties  

    #delete() deletes a node from the Red-Black Tree.
    def delete(self, user_id: int):
        node = self.search(user_id)  #search if the node to be deleted exists in the tree
        if node == self.NIL: #if not, return
            return

        #elseif it exists
        target_node = node
        target_node_original_color = target_node.color

        #case 1: If the node to be deleted has no left child, we replace the node with the right child
        if node.left == self.NIL:
            replace_node = node.right
            self._transplantion(node, node.right)
        #case 1: If the node to be deleted has no right child, we replace the node with the left child    
        elif node.right == self.NIL:
            replace_node = node.left
            self._transplantion(node, node.left)
        #If the node to be deleted has both children, we find min node in right subtree and it becomes the successor    
        else:
            target_node = self._find_minimum_node(node.right)
            target_node_original_color = target_node.color
            replace_node = target_node.right

            if target_node.parent == node:
                replace_node.parent = target_node
            else:
                self._transplantion(target_node, target_node.right)
                target_node.right = node.right
                target_node.right.parent = target_node

            self._transplantion(node, target_node)
            target_node.left = node.left
            target_node.left.parent = target_node
            target_node.color = node.color

        if target_node_original_color == 0:
            self._correct_delete_node(replace_node)    #after deletion, we call correct delete node to rebalance and maintain the redblack tree properties

    #_correct_delete_node corrects the Red-Black Tree properties after insertion
    def _correct_insert_node(self, new_node):
        while new_node.parent and new_node.parent.color == 1:  #while loop continues till new parent is red
            
            #Case 1: checks if the parent is the right child of grandparent
            if new_node.parent == new_node.parent.parent.right:
                unc_node = new_node.parent.parent.left

                #Case 1.1: if uncle is red, we change the colors of the uncle and parent to black, and the grandparent to red and moves up the tree by setting the new node to be the grandparent.
                if unc_node.color == 1:
                    unc_node.color = 0
                    new_node.parent.color = 0
                    new_node.parent.parent.color = 1
                    new_node = new_node.parent.parent

                #Case 1.2: if uncle is black, if the new node is a left child, the function performs a right rotation on the parent, changes the parent's color to black and grandparent's to red, and then performs a left rotation on the grandparent to maintain the Red-Black Tree properties.    
                else:
                    if new_node == new_node.parent.left:
                        new_node = new_node.parent
                        self._right_rotation(new_node)

                    new_node.parent.color = 0
                    new_node.parent.parent.color = 1
                    self._left_rotation(new_node.parent.parent)

            #Case 2: checks if the parent is the left child of grandparent
            else:
                unc_node = new_node.parent.parent.right

                #Case 2.1: if uncle is red, we change the colors of the uncle and parent to black, and the grandparent to red and moves up the tree by setting the new node to be the grandparent.
                if unc_node.color == 1:
                    unc_node.color = 0
                    new_node.parent.color = 0
                    new_node.parent.parent.color = 1
                    new_node = new_node.parent.parent

                #Case 1.2: if uncle is black, if the new node is a right child, the function performs a left rotation on the parent, changes the parent's color to black and grandparent's to red, and then performs a right rotation on the grandparent to maintain the Red-Black Tree properties.        
                else:
                    if new_node == new_node.parent.right:
                        new_node = new_node.parent
                        self._left_rotation(new_node)

                    new_node.parent.color = 0
                    new_node.parent.parent.color = 1
                    self._right_rotation(new_node.parent.parent)

            if new_node == self.root:  #we break if the new node becomes the root node
                break

        self.root.color = 0    

    #_correct_delete_node() fixes the Red-Black Tree properties after deletion.
    def _correct_delete_node(self, fix_node):
        while fix_node != self.root and fix_node.color == 0:

            #Case 1: If the fix_node is the left child of its parent
            if fix_node == fix_node.parent.left:
                sibling_node = fix_node.parent.right

                #Case 1.1: If sibling is red, we change the sibling color to black and parent's to red, then we perform left rotation on the parent and finally update the sibling to be the new right child of the parent 
                if sibling_node.color == 1:
                    sibling_node.color = 0
                    fix_node.parent.color = 1
                    self._left_rotation(fix_node.parent)
                    sibling_node = fix_node.parent.right

                #Case 1.2: If both of the sibling's children are black, we change the sibling's color to red and move it up the tree by setting fix_node to its parent
                if sibling_node.left.color == 0 and sibling_node.right.color == 0:
                    sibling_node.color = 1
                    fix_node = fix_node.parent

                #Case 1.3: If the sibling's right child is black, we change the sibling's left child to black and the sibling to red. Performs a right rotation on the sibling and update the sibling to be the new right child of the parent    
                else:
                    if sibling_node.right.color == 0:
                        sibling_node.left.color = 0
                        sibling_node.color = 1
                        self._right_rotation(sibling_node)
                        sibling_node = fix_node.parent.right

                    sibling_node.color = fix_node.parent.color
                    fix_node.parent.color = 0
                    sibling_node.right.color = 0
                    self._left_rotation(fix_node.parent)
                    fix_node = self.root

            #Case 2: If the fix_node is the right child of its parent
            else:
                sibling_node = fix_node.parent.left
                #Case 2.1: If sibling is red, we change the sibling color to black and parent's to red, then we perform right rotation on the parent and finally update the sibling to be the new left child of the parent 
                if sibling_node.color == 1:
                    sibling_node.color = 0
                    fix_node.parent.color = 1
                    self._right_rotation(fix_node.parent)
                    sibling_node = fix_node.parent.left

                #Case 2.2: If both of the sibling's children are black, we change the sibling's color to red and move it up the tree by setting fix_node to its parent
                if sibling_node.right.color == 0 and sibling_node.left.color == 0:
                    sibling_node.color = 1
                    fix_node = fix_node.parent

                #Case 3.3: If the sibling's right child is black, we change the sibling's left child to black and the sibling to red. Performs a left rotation on the sibling and update the sibling to be the new left child of the parent    
                else:
                    if sibling_node.left.color == 0:
                        sibling_node.right.color = 0
                        sibling_node.color = 1
                        self._left_rotation(sibling_node)
                        sibling_node = fix_node.parent.left

                    sibling_node.color = fix_node.parent.color
                    fix_node.parent.color = 0
                    sibling_node.left.color = 0
                    self._right_rotation(fix_node.parent)
                    fix_node = self.root

        fix_node.color = 0    

    #inorder_traversal() returns an inorder traversal of the tree.
    def inorder_traversal(self):
        result = []   #initilize empty list
        self._inorder_helper(self.root, result) #calls inorder helper which traverse first to right, then root then left
        return result    
    
    #_right_rotation() performs a right rotation on the given node.
    def _right_rotation(self, gp_node):
        # Set father_node as the left child of gp_node
        father_node = gp_node.left
        # Move the right subtree of father_node to the left subtree of gp_node
        gp_node.left = father_node.right

        # Update the parent of the moved subtree if it exists
        if father_node.right != self.NIL:
            father_node.right.parent = gp_node

        # Update father_node's parent to be gp_node's parent
        father_node.parent = gp_node.parent

        # If gp_node was the root, update the root
        if gp_node.parent is None:
            self.root = father_node
        # else update the correct child of gp_node's parent
        elif gp_node == gp_node.parent.right:
            gp_node.parent.right = father_node
        else:
            gp_node.parent.left = father_node

        # Make gp_node the right child of father_node
        father_node.right = gp_node
        gp_node.parent = father_node

    #_left_rotation() performs a left rotation on the given node.
    def _left_rotation(self, gp_node):
        # Set father_node as the right child of gp_node
        father_node = gp_node.right
        # Move the left subtree of father_node to the right subtree of gp_node
        gp_node.right = father_node.left

        # Update the parent of the moved subtree if it exists
        if father_node.left != self.NIL:
            father_node.left.parent = gp_node

        # Update father_node's parent to be gp_node's parent
        father_node.parent = gp_node.parent

        # If gp_node was the root, update the root
        if gp_node.parent is None:
            self.root = father_node
        # else, update the correct child of gp_node's parent
        elif gp_node == gp_node.parent.left:
            gp_node.parent.left = father_node
        else:
            gp_node.parent.right = father_node

        # Make gp_node the left child of father_node
        father_node.left = gp_node
        gp_node.parent = father_node

    #inorder_helper() helps the inorder_traversal() to traversal and keep in order
    def _inorder_helper(self, node, result):
        # Base case: if the current node is not NIL (sentinel node)
        if node != self.NIL:
            # Recursively traverse the left subtree
            self._inorder_helper(node.left, result)
            
            # Process the current node: append its seat_id and user_id to the result list
            result.append((node.seat_id, node.user_id))
            
            # Recursively traverse the right subtree
            self._inorder_helper(node.right, result)
  
    #_transplantion() replaces one subtree with another.
    def _transplantion(self, old_node, replace_node):
        # If old_node is the root, update the root to be replace_node
        if old_node.parent is None:
            self.root = replace_node
        # If old_node is a left child, update its parent's left child to be replace_node
        elif old_node == old_node.parent.left:
            old_node.parent.left = replace_node
        # If old_node is a right child, update its parent's right child to be replace_node
        else:
            old_node.parent.right = replace_node

        # Set the parent of replace_node to be the parent of old_node
        replace_node.parent = old_node.parent

    #_find_minimum_node() finds the minimum node in a subtree.
    def _find_minimum_node(self, node):
        # Traverse the left child pointers until we reach the leftmost node
        while node.left != self.NIL:
            node = node.left
        # Return the leftmost node, which has the minimum key in the subtree
        return node

#MinHeap class implements a Min Heap for managing the waitlist.
class MinHeap:
    #__init__() is the constructor for the MinHeap class. 
    def __init__(self):
        self.heap = [] #Heap list is used for storing elements of the heap
        self.entry_count = 0 #The entry_count is keeping track of the order in which elements are added to the heap
        self.user_index = {} #The user_index dictionary keeping track of the index of each user in the heap

    #insert() inserts a new entry into the heap.
    def insert(self, priority, user_id):
        # Create entry with priority, timestamp and the user_id
        entry = [priority, self.entry_count, user_id] # a new entry is created with the details passed from the input file
        self.heap.append(entry) #this entry is appended at the end of the heap
        self.user_index[user_id] = len(self.heap) - 1 
        self.entry_count += 1
        self._heapify_up(len(self.heap) - 1) #after insertion of new node in the heap, we call heapify_up() to correct and maintain heap properties

    #compare() compares two heap entries.
    def _compare(self, node1, node2):
        # First we compare the nodes by priority, per test case observation, I have build in a way where the higher number means higher priority
        if node1[0] != node2[0]:
            return node2[0] - node1[0]
        # Then we compare them by the entry time. The earlier entry wins
        return node1[1] - node2[1]     

    #extract_min() extracts and returns the minimum element from the heap
    def extract_min(self):
        if not self.heap: #if heap is empty, return none
            return None

        #if heap not empty
        min_item = self.heap[0] #min_item stores the minimum element (we are deleting the min element)
        last_item = self.heap.pop() #pop the last element in the heap
        
        if self.heap:
            self.heap[0] = last_item #the last element is placed at the top which is the min place
            self.user_index[last_item[2]] = 0 
            self._heapify_down(0) #and then we call heapify_down to adjust and maintain heap properties which will take the currently top element down and it will get further replaced by the corresponding nodes
        
        del self.user_index[min_item[2]]
        return min_item #we give back the min element from the waiting list so they can get a seat 
    
    # remove() removes a specific user from the heap.
    def remove(self, user_id):
        if user_id not in self.user_index:   #checks if the user exists
            return False
        
        #here in the user to be deleted exisits, we move the last person in line to that spot, updates their position, and then removes the last spot in line
        index = self.user_index[user_id]
        self.heap[index] = self.heap[-1]
        self.user_index[self.heap[-1][2]] = index
        self.heap.pop()
        
        #After removing the user, we check if the heap needs any rebalancing by comparing the replaced element with its parent.
        #if rebalancing is required, we call either _heapify_up() to move it up or _heapify_down() to move it down, ensuring the heap property is maintained.
        if len(self.heap) > 0 and index < len(self.heap):
            if index > 0 and self._compare(self.heap[index], self.heap[(index-1)//2]) < 0:
                self._heapify_up(index)
            else:
                self._heapify_down(index)
        
        del self.user_index[user_id]
        return True

    #update_priority() updates the priority of a user in the heap
    def update_priority(self, user_id, new_priority):
        if user_id not in self.user_index:      #checks if the user exists
            return False
        
        #if the user exists, we update its priority and then check if the new priority is greater than old priority. 
        #if it is greater, we call heapify_up() else heapify_down()
        index = self.user_index[user_id]
        old_priority = self.heap[index][0]
        self.heap[index][0] = new_priority
        if new_priority > old_priority:
            self._heapify_up(index)  #moves node up
        else:
            self._heapify_down(index) #moves node down
        return True
    
    #heapify_up maintains the heap property by moving an element up.
    def _heapify_up(self, index):
        parent = (index - 1) // 2
        while index > 0 and self._compare(self.heap[index], self.heap[parent]) < 0:
            # Swap the nodes if the parent is bigger than the child node
            self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]
            # Update their indices
            self.user_index[self.heap[index][2]] = index
            self.user_index[self.heap[parent][2]] = parent
            index = parent
            parent = (index - 1) // 2

    #heapify_down() maintains the heap property by moving an element down
    def _heapify_down(self, index):
        while True:
            smallest = index
            left = 2 * index + 1
            right = 2 * index + 2

            if left < len(self.heap) and self._compare(self.heap[left], self.heap[smallest]) < 0:
                smallest = left
            if right < len(self.heap) and self._compare(self.heap[right], self.heap[smallest]) < 0:
                smallest = right

            if smallest == index:
                break

            #swap current element with the smaller child, to ensure the element sinks to its correct position in the min-heap, maintaining the heap property
            self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
            self.user_index[self.heap[index][2]] = index
            self.user_index[self.heap[smallest][2]] = smallest
            index = smallest    

#GatorTicketMaster Class implements the main ticket reservation system
class GatorTicketMaster:
     
    def __init__(self):
        self.reserved_seats = RedBlackTree()  #Creates a new instance of the RedBlackTree class to manage reserved seats
        self.waitlist = MinHeap() #Initializes a MinHeap to manage the waitlist
        self.available_seats = [] #empty list to keep track of available (unassigned) seats
        self.seat_count = 0 #initializes a counter for the total number of seats

    #init() initializes the system with a given number of seats
    def initialize(self, seat_count: int):
        #if number of seats entered are less than or equal to 0
        if seat_count <= 0:
            return "Invalid input. Please provide a valid number of seats."
        self.seat_count = seat_count
        self.available_seats = list(range(1, seat_count + 1))
        return f"{seat_count} Seats are made available for reservation"

    #reserve() handles seat reservations or adds users to the waitlist
    def reserve(self, user_id: int, user_priority: int):
        if self.available_seats:  # check for any available seats
            seat = self.available_seats.pop(0)  #pop the available seats
            self.reserved_seats.insert(user_id, seat) #assign the seats to the user
            return f"User {user_id} reserved seat {seat}"
        else:
            self.waitlist.insert(user_priority, user_id) #if there are no seats available, then add to the waitlist
            return f"User {user_id} is added to the waiting list"   

    #available() returns the number of available seats and waitlist size.
    def available(self):
        return f"Total Seats Available : {len(self.available_seats)}, Waitlist : {len(self.waitlist.heap)}"     

    #add_seats() adds new seats to the system and assigns them to waitlisted users if possible
    def add_seats(self, count: int):
        if count <= 0:
            return "Invalid input. Please provide a valid number of seats."
        
        new_seat_start = self.seat_count + 1
        self.seat_count += count
        result = f"Additional {count} Seats are made available for reservation"
        
        # Store waitlist entries temporarily to maintain correct order
        waitlist_entries = []
        while self.waitlist.heap:
            waitlist_entries.append(self.waitlist.extract_min())
            
        # Process waitlist in priority order
        new_seats = list(range(new_seat_start, self.seat_count + 1))
        seat_idx = 0
        
        for entry in waitlist_entries:
            if seat_idx < len(new_seats):
                self.reserved_seats.insert(entry[2], new_seats[seat_idx])
                result += f"\nUser {entry[2]} reserved seat {new_seats[seat_idx]}"
                seat_idx += 1
            else:
                # Put back in waitlist if no seat available
                self.waitlist.insert(entry[0], entry[2])
                
        # Add remaining seats to available_seats
        while seat_idx < len(new_seats):
            self.available_seats.append(new_seats[seat_idx])
            seat_idx += 1
            
        self.available_seats.sort()
        return result    

    #cancel() cancels a reservation and handles waitlist if necessary.
    def cancel(self, seat_id: int, user_id: int):
        node = self.reserved_seats.search(user_id)  #search user in the reserved seat

        if node and node.seat_id == seat_id:  #if user is available in the reserved seat list, delete them from the list
            self.reserved_seats.delete(user_id)
            result = f"User {user_id} canceled their reservation"

            if self.waitlist.heap:   #after cancellation, if waitlist is not empty, check if any other user in the waitlist, if so, assign then the seat
                next_user = self.waitlist.extract_min()
                self.reserved_seats.insert(next_user[2], seat_id)
                result += f"\nUser {next_user[2]} reserved seat {seat_id}"
            else:
                self.available_seats.append(seat_id)  #if waitlist is empty, give them the seat
                self.available_seats.sort()
            return result
        
        return f"User {user_id} has no reservation for seat {seat_id} to cancel"
    
    #update_priority() updates a user's priority in the waitlist
    def update_priority(self, user_id: int, user_priority: int):
        if self.waitlist.update_priority(user_id, user_priority): #updates priority of the user
            return f"User {user_id} priority has been updated to {user_priority}"
        
        if self.reserved_seats.search(user_id) != self.reserved_seats.NIL: #user's priority cannot be updated successfully
            return f"User {user_id} priority is not updated"
        
        return f"User {user_id} is not in the system"

    #print_reservation() prints all current reservations
    def print_reservations(self):
        return "\n".join([f"Seat {seat_id}, User {user_id}" for seat_id, user_id in sorted(self.reserved_seats.inorder_traversal())])

    #release_seats() releases seats for a range of user IDs and reassigns them to waitlisted users
    def release_seats(self, user_id1: int, user_id2: int):
        # Check if the range is valid
        if user_id1 > user_id2:
            return "Invalid input. Please provide a valid range of users."
        
        released_seats = []
        stack = []
        current = self.reserved_seats.root
        
        # we collect all seats to be released using an in-order traversal
        while current != self.reserved_seats.NIL or stack:
            while current != self.reserved_seats.NIL:
                stack.append(current)
                current = current.left
            current = stack.pop()
            if user_id1 <= current.user_id <= user_id2:
                released_seats.append((current.seat_id, current.user_id))
            if current.user_id > user_id2:
                break  # break if we gone past the range
            current = current.right
        
        result = []
        # we check if there are seats to release or users in the waitlist within the range
        if released_seats or any(user_id1 <= user[2] <= user_id2 for user in self.waitlist.heap):
            result.append(f"Reservations of the Users in the range [{user_id1}, {user_id2}] are released")
            
            # Release seats from the Red-Black Tree
            for seat_id, user_id in released_seats:
                self.reserved_seats.delete(user_id)
                self.available_seats.append(seat_id)
            
            # Remove users from the waitlist if they're in the specified range
            self.waitlist.heap = [user for user in self.waitlist.heap if not (user_id1 <= user[2] <= user_id2)]
            self.waitlist.user_index = {user[2]: i for i, user in enumerate(self.waitlist.heap)}
            
            # Sort available seats to maintain order
            self.available_seats.sort()
            
            # Reassign available seats to users in the waitlist
            while self.available_seats and self.waitlist.heap:
                next_seat = self.available_seats.pop(0)
                next_user = self.waitlist.extract_min()
                self.reserved_seats.insert(next_user[2], next_seat)
                result.append(f"User {next_user[2]} reserved seat {next_seat}")

        if result:
            return "\n".join(result)
        return f"No reservations or waitlist entries found in the range [{user_id1}, {user_id2}]"

    #exit_waitlist() removes a user from the waitlist
    def exit_waitlist(self, user_id: int):
        # remove the user from the waitlist
        if self.waitlist.remove(user_id):
            # if removal is successful
            return f"User {user_id} is removed from the waiting list"
        # if the user was not in the waitlist
        return f"User {user_id} is not in waitlist"


#gator_ticket_commands() processes commands from an input file and writes results to an output file            
def gator_ticket_commands(input_file: str, output_file: str):
    # Initialize the GatorTicketMaster instance
    ticket_master = GatorTicketMaster()
    
    # Open input and output files
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            # Strip whitespace and skip empty lines
            line = line.strip()
            if not line:
                continue
            
            # Parse the command and arguments
            command, *args = line.split('(')
            args = args[0][:-1] if args else ''
            args = list(map(int, args.split(','))) if args else []

            result = ""
            # Process each command
            if command == 'Initialize' and len(args) == 1:
                result = ticket_master.initialize(args[0])
                
            elif command == 'Reserve' and len(args) == 2:
                result = ticket_master.reserve(args[0], args[1])

            elif command == 'Available':
                result = ticket_master.available()    

            elif command == 'AddSeats' and len(args) == 1:
                result = ticket_master.add_seats(args[0])

            elif command == 'Cancel' and len(args) == 2:
                result = ticket_master.cancel(args[0], args[1])  

            elif command == 'UpdatePriority' and len(args) == 2:
                result = ticket_master.update_priority(args[0], args[1])      

            elif command == 'PrintReservations':
                result = ticket_master.print_reservations()

            elif command == 'ReleaseSeats' and len(args) == 2:
                result = ticket_master.release_seats(args[0], args[1])

            elif command == 'ExitWaitlist' and len(args) == 1:
                result = ticket_master.exit_waitlist(args[0])

            elif command == 'Quit':
                result = "Program Terminated!!"
                # Write the result and break the loop
                outfile.write(result + '\n')
                break
            else:
                # Handle unrecognized commands
                result = f"Unrecognized command: {command}"

            # Write the result to the output file
            if result:
                outfile.write(result + '\n')

# The main block handles command-line execution of the program
if __name__ == '__main__':
    # we checks if the correct number of command-line arguments is provided
    if len(sys.argv) != 2:
        print("Incorrect number of input arguments, please follow the usage: python3 gatorTicketMaster.py <input_filename>")
        sys.exit(1)
    
    # Extract the input filename from command-line arguments
    input_file = sys.argv[1]
    
    # Generate the output filename by appending '_output_file.txt' to the input filename without the extension
    output_file = f"{input_file.split('.')[0]}_output_file.txt"
    
    # Call the gator_ticket_commands function to execute the program
    gator_ticket_commands(input_file, output_file)
    #print(f"Output has been written to {output_file}")
