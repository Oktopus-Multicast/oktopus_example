from oktopus import App, Routing, Session, Service

# Application API
app = App(name='Abilene', topo='Abilene_resources.graphml') # Load the network topology

firewall = Service(name='fw', ordered=True, resources_cap={'cpu': 10})
video_transcoder = Service(name='vt', ordered=True, resources_cap={'cpu': 10})
app.get_node(2).add_service(firewall) # add firewall network function to node 2
app.get_node(9).add_service(video_transcoder) # add video transcoder network function to node 9

# Session API
session = Session(addr='192.0.2.0', 
                  src=1, 
                  dsts={8, 2, 7, 9}, 
                  bw=10000000, 
                  t_class='vod',
                  res={'fw':{'cpu': 10}, 'vt':{'cpu': 10}},
                  required_services=['fw', 'vt'] # set service chain
                )

app.add_sessions([session]) # add multicast session


# Routing API
routing = Routing()
routing.add_objective(name='minroutingcost')

routing.add_node_constraint(node=app.get_node(9), srv=video_transcoder, name='cpu', value=5) # limit firewall usage to 5 cpu

app.set_routes(routing)

# Produces a solution
app.solve()

