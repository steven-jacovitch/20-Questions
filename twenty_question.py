class TwentyQuestions:
    def __init__(self, treeFileName=None):
        """
        Initialize the TwentyQuestions class with predefined small and medium trees.
        Sets the current tree to the small tree by default.
        """
        self.smallTree = (
            "Is it bigger than a breadbox?",
            ("an elephant", None, None),
            ("a mouse", None, None),
        )
        self.mediumTree = (
            "Is it bigger than a breadbox?",
            ("Is it gray?", ("an elephant", None, None), ("a tiger", None, None)),
            ("a mouse", None, None),
        )
        self.currentTree = self.smallTree  # Default tree
        self.treeFileName = treeFileName

    def inputChecker(self, userIn: str):
        """
        aka(yes(userIn))
        Check if the user's input is an affirmative response.

        Parameters
        ----------
        userIn : str
            The input string from the user.

        Returns
        -------
        bool
            True if the input is an affirmative response ('y', 'yes', 'yup', 'sure'), else False.
        """

        if userIn.lower() in ["y", "yes", "yup", "sure"]:
            return True
        return False

    def checkIfLeaf(self, curNode):
        """
        Determine if the given node is a leaf node.

        Parameters
        ----------
        curNode : tuple
            The current node in the decision tree.

        Returns
        -------
        bool
            True if the node is a leaf (both children are None), else False.
        """

        if curNode[1] is None and curNode[2] is None:
            return True
        return False


    def simplePlay(self, curNode):
        """
        Conduct a simple playthrough of the game using the current node.

        Parameters
        ----------
        curNode : tuple
            The current node in the decision tree.

        Returns
        -------
        bool
            True if the player successfully guesses the item, else False.
        """
        # If the tree is a leaf
        if self.checkIfLeaf(curNode):
            # Ask whether the object is the object named in the leaf
            answer = input(f"Is it a {curNode}? (yes/no): ")
            # Return True or False appropriately
            return self.inputChecker(answer)
        else:
            # If the tree is not a leaf, ask the question in the tree
            answer = input(f"{curNode[0]} (yes/no): ")
            if answer.lower() == "yes":
                # If the user answers "yes", call yourself recursively on the subtree that is the second element in the triple
                return self.simplePlay(curNode[1])
            else:
                # If the user answers "no", recur on the subtree that is the third element in the triple
                return self.simplePlay(curNode[2])

    def createNode(
        self, userQuestion: str, userAnswer: str, isCorrectForQues: bool, curNode: tuple
    ):
        """
        Create a new node in the decision tree.

        Parameters
        ----------
        userQuestion : str
            The question to differentiate the new answer from the current node.
        userAnswer : str
            The answer provided by the user.
        isCorrectForQues : bool
            True if the userAnswer is the correct response to the userQuestion.
        curNode : tuple
            The current node in the decision tree at which the game has arrived.
            This node typically represents the point in the game
            where the player's guess was incorrect,
            and a new question-answer pair needs to be
            added to refine the tree.


        Returns
        -------
        tuple
            The new node created with the user's question and answer
            and curNode
        """
        # If the user's answer is correct for the current question
        if isCorrectForQues:
            return (userQuestion, (userAnswer, None, None), curNode)
        else: # If the user's answer is incorrect for the current question
            return (userQuestion, curNode, (userAnswer, None, None))

    def playLeaf(self, curNode):
        """
        Handle gameplay when a leaf node is reached in the decision tree. This method is called when
        the game's traversal reaches a leaf node, indicating a guess at the player's thought.
        If the guess is incorrect, the method will
        1. prompts the player for the correct answer
        2. prompts the player for a distinguishing question
        3. ask user what is the answer for the new input item to this distinguishing question(refer the io result of play in the homework doc)
           notice the node should follow (tree question, (node for answer yes), (node for answer no))
        4. creating a new node in the tree for future gameplay. It should call self.createNode(...)

        Parameters
        ----------
        curNode : tuple
            The current leaf node in the decision tree. A leaf node is represented as a tuple with the guessed
            object as the first element and two `None` elements, signifying that it has no further branches.

        Returns
        -------
        tuple
            The updated node based on user input. If the player's response indicates that the initial guess was
            incorrect, this method returns a new node that includes the correct answer and a new question
            differentiating it from the guessed object. If the guess was correct, it simply returns the unchanged
            `curNode`.

        Notes
        -----
        The method interacts with the player to refine the decision tree. It's a crucial part of the learning
        aspect of the game, enabling the tree to expand with more nuanced questions and answers based on
        player feedback.
        """

        guess = curNode[0]
        answer = input(f"Is it {guess}? (yes/no): ")
        if self.inputChecker(answer):
            print("Hooray! I guessed correctly!")
            return curNode
        else:
            print("Oh no! I'll try to do better next time.")
            correct_answer = input("What was the correct answer? ")
            new_question = input(f"Please enter a question that distinguishes {guess} from {correct_answer}: ")
            answer_to_new_question = input(f"For {correct_answer}, what would the answer to your question be? (yes/no): ")
            if self.inputChecker(answer_to_new_question):
                return (new_question, (correct_answer, None, None), curNode)
            else:
                return (new_question, curNode, (correct_answer, None, None))

    def play(self, curNode):
        """
        Conduct gameplay starting from the given node.

        Parameters
        ----------
        curNode : tuple
            The current node in the decision tree.

        Returns
        -------
        tuple
            The updated tree after playing from the given node.
        """
        # If the tree is a leaf
        if self.checkIfLeaf(curNode):
            # Handle gameplay when a leaf node is reached
            new_subtree = self.playLeaf(curNode)
            self.currentTree = new_subtree
            return new_subtree
        else:
            # If the tree is not a leaf, ask the question in the tree
            answer = input(f"{curNode[0]} (yes/no): ")
            if self.inputChecker(answer):
                # If the user answers "yes", call yourself recursively on the subtree that is the second element in the triple
                if curNode[1] is not None:
                    new_subtree = self.play(curNode[1])
                    self.currentTree = (curNode[0], new_subtree, curNode[2])
                    return self.currentTree
            else:
                # If the user answers "no", recur on the subtree that is the third element in the triple
                if curNode[2] is not None:
                    new_subtree = self.play(curNode[2])
                    self.currentTree = (curNode[0], curNode[1], new_subtree)
                    return self.currentTree

    def playRound(self):
        """
        Execute a single round of the game, starting from the current state of the currentTree attribute. This method
        calls the 'play' method to navigate through the tree. It then updates the 'currentTree'
        attribute with the potentially modified tree resulting from this round of gameplay.


        Returns
        -----
        None
        """
        # Play the game starting from the current tree
        self.currentTree = self.play(self.currentTree)

    def saveTree(self, node, treeFile):
        """
        Recursively save the decision tree to a file.

        Parameters
        ----------
        node : tuple
            The current node in the decision tree.
        treeFile : _io.TextIOWrapper
            The file object where the tree is to be saved.
        """
        if self.checkIfLeaf(node):
            treeFile.write("Leaf\n")
            treeFile.write(node[0] + "\n")
        else:
            treeFile.write("Internal node\n")
            treeFile.write(node[0] + "\n")
            self.saveTree(node[1], treeFile)
            self.saveTree(node[2], treeFile)

    def saveGame(self, treeFileName):
        """
        Save the current state of the game's decision tree to a specified file. This method opens the file
        with the given filename and writes the structure of the current decision tree to it. The tree is saved
        in a txt format.

        The method uses the 'saveTree' function to perform the recursive traversal and writing of the tree
        structure. Each node of the tree is written to the file with its type ('Leaf' or 'Internal node')
        followed by its content (question or object name).

        Important: the format of the txt file should be exactly the same as the ones in our doc to pass the autograder.

        Parameters
        ----------
        treeFileName : str
            The name of the file where the current state of the decision tree will be saved. The file will be
            created or overwritten if it already exists.

        """
        
        with open(treeFileName, "w") as f:
            self.saveTree(self.currentTree, f)

    def loadTree(self, treeFile):
        """
        Recursively read a binary decision tree from a file and reconstruct it.

        Parameters
        ----------
        treeFile : _io.TextIOWrapper
            An open file object to read the tree from.

        Returns
        -------
        tuple
            The reconstructed binary tree.
        """
        # Read the type of the node
        node_type = treeFile.readline().strip()
        # If we've reached the end of the file, return None
        if not node_type:
            return None
        # Read the content of the node
        node_content = treeFile.readline().strip()

        # If the node is a leaf
        if node_type == "Leaf":
            # Return a leaf node with the object name
            return (node_content, None, None)
        else:
            # If the node is not a leaf, read the subtrees recursively
            yes_subtree = self.loadTree(treeFile)
            no_subtree = self.loadTree(treeFile)
            # Return an internal node with the question and subtrees
            return (node_content, yes_subtree, no_subtree)

    def loadGame(self, treeFileName):
        """
        Load the game state from a specified file and update the current decision tree. This method opens the
        file with the given filename and reconstructs the decision tree based on its contents.

        The method employs the 'loadTree' function to perform recursive reading of the tree structure from the
        file. Each node's type ('Leaf' or 'Internal node') and content (question or object name) are read and
        used to reconstruct the tree in memory. This restored tree becomes the new 'self.currentTree' of the game.

        Parameters
        ----------
        treeFileName : str
            The name of the file from which the game state will be loaded. The file should exist and contain a
            previously saved decision tree.

        """
        # Open the file in read mode
        with open(treeFileName, 'r') as f:
            self.currentTree = self.loadTree(f)

    def printTree(self):
        self._printTree(tree=self.currentTree)

    def _printTree(self, tree, prefix="", bend="", answer=""):
        """Recursively print a 20 Questions tree in a human-friendly form.
        TREE is the tree (or subtree) to be printed.
        PREFIX holds characters to be prepended to each printed line.
        BEND is a character string used to print the "corner" of a tree branch.
        ANSWER is a string giving "Yes" or "No" for the current branch."""
        text, left, right = tree
        if left is None and right is None:
            print(f"{prefix}{bend}{answer}It is {text}")
        else:
            print(f"{prefix}{bend}{answer}{text}")
            if bend == "+-":
                prefix = prefix + "| "
            elif bend == "`-":
                prefix = prefix + "  "
            self._printTree(left, prefix, "+-", "Yes: ")
            self._printTree(right, prefix, "`-", "No:  ")


def main():
    """DOCSTRING!"""
    # Write the "main" function for 20 Questions here.  Although
    # main() is traditionally placed at the top of a file, it is the
    # last function you will write.

    print("Welcome to 20 Questions!")

    load_tree = input("Would you like to load a tree from a file? (yes/no): ")
    if load_tree.lower() == "yes":
        filename = input("What's the name of the file? ")
        game = TwentyQuestions(filename)
        game.loadGame(filename)
    else:
        game = TwentyQuestions()

    play_again = "yes"
    while play_again.lower() == "yes":
        game.play(game.currentTree)
        play_again = input("Would you like to play again? (yes/no): ")

    save_tree = input("Would you like to save this tree for later? (yes/no): ")
    if save_tree.lower() == "yes":
        filename = input("Please enter a file name: ")
        game.saveGame(filename)
        print("Thank you! The file has been saved.")
    game.printTree()
    print("Bye")


if __name__ == "__main__":
    main()
