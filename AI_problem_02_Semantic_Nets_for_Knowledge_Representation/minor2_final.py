# import libraries
import plotly.graph_objs as go
import networkx as nx
import random
import re

#-------------------------------------Functions decleration----------------------------------------------
"""#define visualization method"""

def showNet(education_net):
    print("Nodes:", education_net.nodes())
    print("Edges:", education_net.edges())

    # Create a layout for the nodes
    # using Kamada-Kawai layout
    pos = nx.kamada_kawai_layout(education_net)


    # Prepare edge and node traces for Plotly
    edge_x = []
    edge_y = []
    edge_labels = []
    for edge in education_net.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
        edge_labels.append(education_net.edges()[edge]['label'])  # Extract edge labels from networkx graph


    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines'
    )



    node_x = []
    node_y = []
    text = []
    for node in education_net.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        text.append(node)

    node_trace = go.Scatter(
    x=node_x, y=node_y,
    mode='markers+text',
    text=text,
    marker=dict(showscale=False, color='white', size=37,  # Set the color to 'white'
                colorbar=dict(thickness=15, title='Node Connections', xanchor='left'), line_width=2),
    textfont=dict(size=8, color='black', family='Arial'),
)

    # Add edge labels to the edge_trace
    edge_trace.text = edge_labels
    edge_trace.textposition = 'middle right'  # Set the position of edge labels

    # Create a figure
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title='Semantic Net - Education Domain',
                        titlefont_size=16,
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=0, l=0, r=0, t=0),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )

    # Add annotations for edge labels
    annotations = []
    for edge in education_net.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        annotation = dict(
            x=(x0 + x1) / 2,
            y=(y0 + y1) / 2,
            text=education_net.edges()[edge]['label'],
            showarrow=False,
            font=dict(size=8, color='blue'),
            xref='x',
            yref='y'
        )
        annotations.append(annotation)

    fig.update_layout(annotations=annotations)

    # Show the figure
    fig.show()

"""#implementation of main required functions"""

# -----------------------add node------------------------------
def add_node(education_net, file):\
    # --------------function logic----------------
    # take input '1 node' from user according to the format
    # check if node already exist? if yes print message and return
    # if node is new, write it to file & add it to graph
    pattern = r'(Course|Student|Major|Teacher)\s\d+'
    print('\n available node types to add are: (Student, Course, Teacher, Major) \nthe formate should be: -Node Number-, for example: Course 1')
    new_node = input("Enter the new node to add: ")

    if not re.match(pattern, new_node):
      print("invalid input format, try again next time")
      return

    if new_node in education_net.nodes():
        print("Node", new_node, "already exists in the graph")
    else:
        file.write("Node: " + new_node + "\n")
        education_net.add_node(new_node)
        print("Node", new_node, "added successfully.")

# -----------------------delete node------------------------------
def delete_node(education_net, file):
    # --------------function logic----------------
    # take input '1 node' from user according to the format
    # check if node already exist? if no print message and return
    # if node exist, delete it from file with its relations
    # & delete it from graph
    pattern = r'(Course|Student|Major|Teacher)\s\d+'
    print('\n available node types to delete are: (Student, Course, Teacher, Major) \nthe formate should be: -Node Number-, for example: Course 1')
    node_to_delete = input("Enter the node to delete: ")

    if not re.match(pattern, node_to_delete):
      print("invalid input format, try again next time")
      return

    if not education_net.has_node(node_to_delete):
        print("Node", node_to_delete, "does not exist in the graph.")
        return

    # Read the content of the file
    with open('input.txt', 'r') as file_read:
        lines = file_read.readlines()

    # Rewrite the file without the line to be deleted
    with open('input.txt', 'w') as file_write:
        for line in lines:
            if not node_to_delete in line:
                file_write.write(line)

    education_net.remove_node(node_to_delete)
    print("Node", node_to_delete, "deleted successfully.")

# -----------------------add relation------------------------------
def add_relation(education_net, file):
    # --------------function logic----------------
    # take input '1 relation' from user according to the format
    # check if relation already exist? if yes print message and return
    # if relation dosen't exit, add it to file & add it to graph with label

    pattern = r'(Course|Student|Major|Teacher|Faculty)\s\d+\s(->){1}\s(Course|Student|Major|Teacher|Faculty)\s\d+'


    print('\n available node types to be in relation are: (Student, Course, Teacher, Major) \nthe formate should be: -Node Number -> Node Number-, for example: Course 1 -> Teacher 1')
    relation_input = input("Enter the relation in the format 'Node 1 -> Node 2': ")

    if not re.match(pattern, relation_input):
          print("invalid input format, try again next time")
          return

    node1 = ''
    node2 = ''
    node1, node2 = relation_input.split(' -> ')
    if not education_net.has_node(node1):
          print("Node", node1, "does not exist in the graph.")
          return

    if not education_net.has_node(node2):
          print("Node", node2, "does not exist in the graph.")
          return

    if education_net.has_edge(node1, node2):
          print("Relation", relation_input, "already exists in the graph.")
    else:
          edge = (node1, node2)
          if ("Student" in edge[0] and "Course" in edge[1]) or ("Course" in edge[0] and "Student" in edge[1]):
            this_label = 'studies'
            education_net.add_edge(*edge, label = this_label)
          elif ("Teacher" in edge[0] and "Course" in edge[1]) or ("Course" in edge[0] and "Teacher" in edge[1]):
            this_label = 'Teaches'
            education_net.add_edge(*edge, label = this_label)
          elif ("Course" in edge[0] and "Course" in edge[1]) or ("Course" in edge[0] and "Course" in edge[1]):
            this_label = 'prerequisite'
            education_net.add_edge(*edge, label = this_label)
          elif ("Major" in edge[0] and "Course" in edge[1]) or ("Course" in edge[0] and "Major" in edge[1]):
            this_label = 'has course'
            education_net.add_edge(*edge, label = this_label)
          elif ("Major" in edge[0] and "Faculty" in edge[1]) or ("Faculty" in edge[0] and "Major" in edge[1]):
            this_label = 'has major'
            education_net.add_edge(*edge, label = this_label)
          else:
            print('this relation cannot be added, it violates the education_net regulations')
            return
          relation = "Relation: {} -> {}".format(node1, node2)
          file.write(relation + "\n")
          print("Relation", relation_input, "added successfully.")


# -----------------------delete relation------------------------------
def delete_relation(education_net, file):
    # --------------function logic----------------
    # take input '1 relation' from user according to the format
    # check if relation already exist? if no print message and return
    # if relation exits, delete it from file & delete it from graph
    pattern = r'(Course|Student|Major|Teacher|Faculty)\s\d+\s(->){1}\s(Course|Student|Major|Teacher|Faculty)\s\d+'


    print('\n available node types to be in relation are: (Student, Course, Teacher, Major) \nthe formate should be: -Node Number -> Node Number-, for example: Course 1 -> Teacher 1')
    relation_input = input("Enter the relation in the format 'Node 1 -> Node 2': ")


    if not re.match(pattern, relation_input):
      print("invalid input format, try again next time")
      return

    node1 = ''
    node2 = ''
    node1, node2 = relation_input.split(' -> ')

    if not education_net.has_node(node1):
        print("Node", node1, "does not exist in the graph.")
        return

    if not education_net.has_node(node2):
        print("Node", node2, "does not exist in the graph.")
        return

    if not education_net.has_edge(node1, node2):
        print("Relation", relation_input, "does not exist in the graph.")
        return

    relation = "Relation: {} -> {}\n".format(node1, node2)

    # Read the content of the file
    with open('input.txt', 'r') as file_read:
        lines = file_read.readlines()

    # Rewrite the file without the line to be deleted
    with open('input.txt', 'w') as file_write:
        for line in lines:
            if line != relation:
                file_write.write(line)

    education_net.remove_edge(node1, node2)
    print("Relation", relation_input, "deleted successfully.")

# -----------------------Query------------------------------
def query(education_net):

    print('Choose the type of query:')
    print('1: Query by node name')
    print('2: Query by relation')

    try:
      query_type = int(input('Enter your choice (1 or 2): '))

      if query_type == 1:
          # Query by node name
          print('\nAvailable node types in the graph: Course, Teacher, Major, Faculty, Student')
          current_node = input('Enter a node similar to the following format: Course 1\n to perform a query on it in the graph: ')
          node_exists = education_net.has_node(current_node)

          if node_exists:
              related_nodes = []
              relations = []
              for node in education_net.nodes():
                  if node != current_node and education_net.has_edge(node, current_node):
                      related_nodes.append(node)
                      relations.append(education_net.get_edge_data(node, current_node)['label'])
              print('\nNodes related to', current_node, 'are:\n')
              print(related_nodes)
              print('\nTheir relations to', current_node, 'are:\n')
              print(relations)
          else:
              print("\nNode (", current_node, ") does not exist in the graph.")

      elif query_type == 2:
          # Display available relation labels
          unique_relation_labels = set(data['label'] for _, _, data in education_net.edges(data=True))
          print('\nAvailable relation labels in the graph:')
          print(unique_relation_labels)

          # Query by relation label
          relation_label = input("Enter the relation label to query: ")

          matching_edges = [(node1, node2) for node1, node2, data in education_net.edges(data=True) if data.get('label') == relation_label]

          if not matching_edges:
              print(f"\nNo nodes are connected by the '{relation_label}' relation in the graph.")
          else:
              print(f"\nNodes connected by the '{relation_label}' relation are:")
              for edge in matching_edges:
                  print(edge[0], '->', edge[1])

      else:
          print('Invalid input. Please enter 1 or 2.')
    except:
      print("invalid input, try next time")
    

#-------------------------------------Program start----------------------------------------------
"""# opening and reading from file 'read format' then closing it"""
print('This program implements a semantic net to show the relation of majors, courses and other elements \nin one faculity')
my_file = open('input.txt', 'r')
nodes = []
line_split = []
edges = []
src_dest = []
myTuple = ()
while True:
    # Get next line from file
    line = my_file.readline()
    # if line is empty
    # end of file is reached
    if not line:
        break
    line_split = line.split(':')
    if line_split[0] == 'Node':
      nodes.append(line_split[1].strip())

    elif line_split[0] == 'Relation':
      src_dest = line_split[1].split('->')
      myTuple = (src_dest[0].strip(), src_dest[1].strip())
      edges.append(myTuple)
my_file.close()

"""# create a graph and add nodes"""

education_net = nx.Graph()
education_net.add_nodes_from(nodes)

"""#add edges with thier lables to the net"""

for edge in edges:
  if ("Student" in edge[0] and "Course" in edge[1]) or ("Course" in edge[0] and "Student" in edge[1]):
    this_label = 'studies'
    education_net.add_edge(*edge, label = this_label)
  elif ("Teacher" in edge[0] and "Course" in edge[1]) or ("Course" in edge[0] and "Teacher" in edge[1]):
    this_label = 'Teaches'
    education_net.add_edge(*edge, label = this_label)
  elif ("Course" in edge[0] and "Course" in edge[1]) or ("Course" in edge[0] and "Course" in edge[1]):
    this_label = 'prerequisite'
    education_net.add_edge(*edge, label = this_label)
  elif ("Major" in edge[0] and "Course" in edge[1]) or ("Course" in edge[0] and "Major" in edge[1]):
    this_label = 'has course'
    education_net.add_edge(*edge, label = this_label)
  elif ("Major" in edge[0] and "Faculty" in edge[1]) or ("Faculty" in edge[0] and "Major" in edge[1]):
    this_label = 'has major'
    education_net.add_edge(*edge, label = this_label)

"""# call function for visualization"""

print('showing the current shape of the net: ....')
showNet(education_net)

"""# loop to implement remaining program logic"""

while True:
  print('\n\nchoose an option from the following:')
  print('1: add node')
  print('2: delete node')
  print('3: add relation')
  print('4: delete relation')
  print('5: query')
  print('6: show current net status')
  print('7: exit\n')
  try:
    choice = int(input('enter you choice: '))
    if choice == 1:
      my_file = open('input.txt', 'a')
      add_node(education_net=education_net, file=my_file)
      my_file.close()
    elif choice == 2:
      my_file = open('input.txt', 'r')
      delete_node(education_net=education_net, file=my_file)
      my_file.close()
    elif choice == 3:
      my_file = open('input.txt', 'a')
      add_relation(education_net=education_net, file=my_file)
      my_file.close()
    elif choice == 4:
      my_file = open('input.txt', 'r')
      delete_relation(education_net=education_net, file=my_file)
      my_file.close()
    elif choice == 5:
      query(education_net=education_net)
    elif choice == 6:
      print('showing the current shape of the net: ....')
      showNet(education_net)
    elif choice == 7:
      break
    else:
      print('invalid input')
      continue
  except:
    print("An invalid input detected, try again")
  

"""# final section of the program"""

print("All updates are saved, next time the program runs, the net content will be retrived from the file as you leave it now")
exit()