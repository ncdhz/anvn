class AnvnConfig:

    class AnvnModelOutput:
        
        last_hidden_state='last_hidden_state'
        pooler_output='pooler_output'
        hidden_states='hidden_states'
        attentions='attentions'

        def __init__(self):
            self.last_hidden_state = AnvnConfig.AnvnModelOutput.last_hidden_state
            self.pooler_output = AnvnConfig.AnvnModelOutput.pooler_output
            self.hidden_states = AnvnConfig.AnvnModelOutput.hidden_states
            self.attentions = AnvnConfig.AnvnModelOutput.attentions
            self.output_names = [self.attentions, self.last_hidden_state, self.pooler_output, self.hidden_states]
            
    class AnvnDimName:
        
        data_name = 'data'
        layer_name = 'layer'
        head_name = 'head'

        def __init__(self):
            self.data_name = AnvnConfig.AnvnDimName.data_name
            self.layer_name = AnvnConfig.AnvnDimName.layer_name
            self.head_name = AnvnConfig.AnvnDimName.head_name
    
    def __init__(self):
        self.model_output = self.AnvnModelOutput()
        self.dim_name = self.AnvnDimName()
