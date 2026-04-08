def test_pipeline_runs():
    from pipeline.extractor import Extractor
    
    extractor = Extractor(["EQUIPMENT"])
    result = extractor.extract("Pump failure occurred.")
    
    assert isinstance(result, list)
