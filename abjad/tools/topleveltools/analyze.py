def analyze(argument):
    r'''Makes tonal analysis agent.

    Returns tonal analysis agent.
    '''
    import abjad
    if isinstance(argument, abjad.Component):
        return abjad.tonalanalysistools.TonalAnalysis(argument)
    elif hasattr(argument, '_music'):
        music = argument._music
        return abjad.tonalanalysistools.TonalAnalysis(music)
    else:
        return abjad.tonalanalysistools.TonalAnalysis(argument)
