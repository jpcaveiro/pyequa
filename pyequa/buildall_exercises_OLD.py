def buildall_exercises(self,maxvars=1,silence=True):
        """

        input:

        - maxvars - number of known variables (search exercises with this restriction)


        ```python
        mg = nx.MultiGraph()
        mg.add_edge(1, 2, key="k0")
        'k0'
        mg.add_edge(1, 2, key="k1")
        'k1'
        mg.add_edge(2, 3, key="k0")
        'k0'
        for path in sorted(nx.all_simple_edge_paths(mg, 1, 3)):
            print(path)
        [(1, 2, 'k0'), (2, 3, 'k0')]
        [(1, 2, 'k1'), (2, 3, 'k0')]
        ```

        """

        C = Combinations(self.allvars_list)

        gen = (sv for sv in C if len(sv) <= maxvars)

        dataframe_iloc = -1

        for inputvars_set in gen:

            #Creates edges from ignorance
            #to each var
            for var in inputvars_set:
                #Não funciona porque não adicionar todos os edges
                #Inode_name = Scenario._IGNORANCE_NODE_NAME_
                #Onode_name = self.node_name(set({var}))
                ##add_edge is from nx.DiGraph()
                #self.wisdomgraph.add_edge(Inode_name, Onode_name, name="init.cond.")

                # Coloca aresta temporária partindo
                # da ignorância para cada uma das {var} neste ciclo.
                # Cada aresta tem o rótulo Eq(var,10).
                # Depois averigua se há caminho e anota
                # e remove esta aresta
                self.add_edge_from_solver(
                    SolverCandidate(
                        set({}),  #input set that is Scenario._IGNORANCE_NODE_NAME_
                        set({var}), #output set like {a} (single var)
                        set({SympyRelation(Eq(var,10))}) #10 is not used
                    )
                )

            #TODO: configurar 50,50 de forma automatica
            #self.draw_wisdom_graph(figsize=(50,50))

            #ANTES: Check if has_path
            #has_a_path = nx.has_path(self.wisdomgraph, Scenario._IGNORANCE_NODE_NAME_, Scenario._KNOWLEDGE_NODE_NAME_)
                
            #AGORA: write all paths (each path is an exercise)
            if not silence:
                print("="*10)
                print(f"Caminhos sabendo: {inputvars_set}")
                print("="*10)

            #Shortest
            try:
                node_path_list = list(nx.shortest_path(self.wisdomgraph, Scenario._IGNORANCE_NODE_NAME_, Scenario._KNOWLEDGE_NODE_NAME_))

                #DEBUG
                print("="*10)
                print(f"Caminho sabendo: {inputvars_set}")
                print("="*10)
                for node in node_path_list:
                    print(node)
                #Os primeiros nós são apenas formados por arestas das condições iniciais.

                #DEBUG
                #self.debug_exercise(inputvars_set,node_path_list)


                #outputvars_set = set(self.allvars_list) - set(inputvars_set)

                dataframe_iloc += 1
                self.solverslist_text = self.solverslist_buildtext(inputvars_set,node_path_list,silence)
                teacher_text = self.text_service.build_one(self,inputvars_set,dataframe_iloc)

                if not silence:
                    #For user to imediatly see but
                    #check self.text_service.buildone() for more.
                    print(teacher_text)

                #Debug
                print(teacher_text)                    
                
            except nx.NetworkXNoPath:
                if not silence:
                    #Debug
                    print("    Não há caminho!")

            
            #ALL paths
            #for path in sorted(nx.all_simple_edge_paths(self.wisdomgraph, Scenario._IGNORANCE_NODE_NAME_, Scenario._KNOWLEDGE_NODE_NAME_)):
            #    print(path)

            #Remove (artificial) edges
            for var in inputvars_set:

                self.remove_edge_from_solver(
                    SolverCandidate(
                        set({}),  #input set that is Scenario._IGNORANCE_NODE_NAME_
                        set({var}), #output set like {a} (single var)
                        set({SympyRelation(Eq(var,10))}) #10 is not used
                    )
                )

        return 
        #end of buildall_exercises()
