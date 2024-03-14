def generate_query(
    tenant_id, time_period_days, environment_exclude, meter_name_exclude
):
    query_template = """
XStoreAccountBillingDaily
    | where Tenant == "{tenant_id}" and TimePeriod >= ago({time_period_days}d) and TimePeriod < now() and Environment != "{environment_exclude}" and isnotempty(MeterId)
    | where StgMeterName != "{meter_name_exclude}"
    | summarize ProratedQuantity = sum(ProratedQuantity) by bin(TimePeriod,1d), Tenant
    | project TimePeriod, Tenant, ProratedQuantity
"""

    query = query_template.format(
        tenant_id=tenant_id,
        time_period_days=time_period_days,
        environment_exclude=environment_exclude,
        meter_name_exclude=meter_name_exclude,
    )

    return query


# Example usage
tenant_id = "MS-CBN09PrdStf02C"
time_period_days = 180
environment_exclude = "Test"
meter_name_exclude = "StgBlockBlobArchivePriorityRetrievalOperationUnitsBilled"

query = generate_query(
    tenant_id, time_period_days, environment_exclude, meter_name_exclude
)
print(query)
