def solve(configuration):
    if configuration.is_solved():
        return configuration
    else: 
        for new_configuration in configuration.get_next_configurations():
            if new_configuration.is_valid():
                result = solve(new_configuration)
                if result:
                    return result
    return None