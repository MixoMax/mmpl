# !/usr/bin/python3
#
#%% Comments
#
# Created on: 12/08/2024
# Auther: Linus Horn <linus@linush.org>
# -------------------------------------
#
# Comments and Notes
# ------------------
#
# 12/08/2024 - 15:37
# Example comment
# - Example Author
# 
# 
# 12/08/2024 - 19:49
# This entire codebase was written on an
# Airplane with no internet connection.
# This means that i had no AI autocomplete,
# and, more importantly no language syntax
# reference / documentation.
# This is the reason why i implemented the
# ´add´ operator using a standard ´def´ function
# instead of writing a lambda for it
# because i forgot the syntax for lambdas.
# I think it was something like this:
# > add = lambda x,y: return x+y
# but this did not work and the red squiggles
# were not helpful enough to help me figure it out
# - Linus Horn
#
#
# 12/08/2024 - 19:55
# Time since last message: 6 minutes
# nvm, i figured out the syntax for
# lambda functions in Python.
# It is like this:
# > add = lambda x,y: x+y
# > print(add(3,6))
# > >>>9
# - Linus Horn


#%% actual code



import json
import time



class Operator:
    func: callable

    def __init__(self, func: callable) -> None:
        self.func = func



class TreeNode:
    left: "TreeNode"
    right: "TreeNode"
    
    operator: Operator | None

    result: int | float

    def __init__(
            self,
            left = None,
            right = None,
            operator = None,
            result = None
    ) -> None:
        
        self.left = left
        self.right = right
        self.operator = operator
        self.result = result

    def is_solved(self) -> bool:
        has_children: bool = ((self.left != None) and (self.right != None))

        is_solved = ((not has_children) and (self.result != None))

        return bool(is_solved)
    
    def __solve_self(self):
        func = self.operator.func
        left = self.left
        right = self.right

        are_prepped = ((left.is_solved()) and right.is_solved())
        if not are_prepped:
            raise ValueError("The two children nodes must be solved first")
        
        left_result = left.result
        right_result = right.result

        result_scalar = func(left_result, right_result)
        return result_scalar

    def solve(self) -> "TreeNode":
        if self.is_solved():
            return self.result
        
        left = self.left
        right = self.right

        if left != None:
            if not left.is_solved():
                left = left.solve()
        
        if right != None:
            if not right.is_solved():
                right = right.solve()
        
        self.left = left
        self.right = right

        result_scaler = self.__solve_self()
        
        
        return TreeNode(result=result_scaler)

    def __str__(self) -> str:
        left = self.left
        right = self.right
        operator = self.operator
        result = self.result
        return f"<TreeNode({left=} | {operator=} | {right=} | {result=})>"
    
    def to_json(self) -> dict:
        left = self.left
        right = self.right

        if left != None:
            left_data = left.to_json()
        else:
            left_data = {}
        
        if right != None:
            right_data = right.to_json()
        else:
            right_data = {}
        
        self_data = {}

        if left_data != {}:
            self_data["left"] = left_data
        if right_data != {}:
            self_data["right"] = right_data


        if self.result != None:
            self_data["result"] = self.result
        
        if self.operator != None:
            self_data["operator"] = self.operator.func.__name__
        
        return self_data



add = lambda x,y: x+y

operator_add = Operator(
    func=add
)

node_in = TreeNode(result = 4)

n_out = TreeNode(result = 0)

for _ in range(800):
    n_out = TreeNode(
        left = n_out,
        right = node_in,
        operator=operator_add
    )


t_start_ns = time.perf_counter_ns()


res = n_out.solve().result


t_end_ns = time.perf_counter_ns()

ns_taken = t_end_ns - t_start_ns
ms_taken = ns_taken / 1_000_000

print(f"{ms_taken=}")

