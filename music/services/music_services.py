def mark_as_inspecting(instance) -> None:
    """ Mark as inspecting
    :arg instance: Track or Album instance"""
    instance.status = 'on_inspection'
    instance.save()