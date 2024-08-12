import json



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



def add(x,y):
    return x+y

operator_add = Operator(
    func=add
)

node_1 = TreeNode(result = 1)

n_out = TreeNode(result = 0)

for _ in range(10):
    n_out = TreeNode(
        left = n_out,
        right = node_1,
        operator=operator_add
    )


with open("./tmp.json", "w", encoding="utf-8") as f:
    data = n_out.to_json()
    f.write(json.dumps(data, indent=4))