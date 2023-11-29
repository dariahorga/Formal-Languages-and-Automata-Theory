class Stack(list):
    def init(self):  # initializes the stack as an empty list
            self = []

    def repr(self): ## If the stack is empty, it returns the $ character; otherwise, it concatenates the elements of the stack and reverses the resulting string
        return "$" if self.is_empty() else "".join(self)[::-1]

    def push_left(self, item):  ## pushes elements onto the top of the stack from the left.
        for s in item[::-1]:
            if s != "$":
                self.append(s)
            else:
                return

    def pop_left(self): ## returns the top element of the stack from the left
        return self.pop()

    def is_empty(self):  ##if the stack is empty
        return len(self) == 0


def log_fail():
    print("reject")


def log_pair(state, stack):
    print("%s#%s|" % (state, stack), end="")

def read_input_file(file_path):
    with open(file_path, "r") as f:
        input_lines = f.readlines()

    input_data={}
    input_data["input_string"]=input_lines[0].strip().split("|")

    # Extracting the set of states
    input_data["states"] = input_lines[1].strip().split(",")

    # Extracting the alphabet sigma
    input_data["sigma"] = input_lines[2].strip().split(",")

    # Extracting the finite stack alphabet
    input_data["stack_alphabet"] = input_lines[3].strip().split(",")

    # Extracting the final states
    input_data["final_states"] = input_lines[4].strip().split(",")

    # Extracting the initial state
    input_data["initial_state"] = input_lines[5].strip()

    # Extracting the initial stack symbol
    input_data["initial_symbol"] = input_lines[6].strip()

    # Extracting the transition functions
    transitions = {}
    for line in input_lines[7:]:
        parts = line.strip().split("->")
        current_state, symbol, current_stack = parts[0].split(",")
        next_state, next_stack = parts[1].split(",")
        if (current_state, symbol, current_stack) not in transitions:
            transitions[(current_state, symbol, current_stack)] = []
        transitions[(current_state, symbol, current_stack)].append((next_state, next_stack))
    input_data["transitions"] = transitions

    return input_data

# Example usage
input_file_path = "input.in"
input_data = read_input_file(input_file_path)
print(input_data)
stack = Stack()
failed = False

# start from initial states
q0 = input_data['initial_state'] #initial state
s0 = input_data['initial_symbol'] #initial symbol
log_pair(q0, s0)

for symbol_group in input_data['input_string']:
    symbols = symbol_group.split(",")
    for symbol in symbols:
        #epsilon
      while input_data['transitions'].get((q0, "$", s0)) is not None:
        (q0, s0) = input_data['transitions'].get((q0, "$", s0))[0]
        stack.push_left(s0)
        log_pair(q0, stack)
        if not stack.is_empty():
            s0 = stack.pop_left()
        else:
            failed = True
            break

      # stack not empty, check if transition exists
      if not failed and input_data['transitions'].get((q0, symbol, s0)) is not None:
        (q0, s0) = input_data['transitions'].get((q0, symbol, s0))[0]
        stack.push_left(s0)
        log_pair(q0, stack)
        if not stack.is_empty():
            s0 = stack.pop_left()
        else:
            failed = True
      else:
        failed = True

    # stack empty
    if failed:
        log_fail()
        break

    # epsilon
    if not failed:
    while input_data['transitions'].get((q0, "$", s0)) is not None and q0 not in input_data['final_states']:
        (q0, s0) = input_data['transitions'].get((q0, "$", s0))[0]
        stack.push_left(s0)
        log_pair(q0, stack)
        if not stack.is_empty():
            s0 = stack.pop_left()
        else:
            break
    print('accept' if q0 in input_data['final_states'] else 'reject', end='\n')
    else:
        pass
