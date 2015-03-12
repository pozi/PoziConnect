<img src="http://i.imgur.com/TLMFPUa.png" alt="Groundtruth" width="200">

# Pozi Connect: Advanced Configuration

### 'Gridlocked' Matches

There are certain match combinations in Vicmap that are not easily corrected. In these cases, a multi-assessment record must first be removed prior to the property being re-matched correctly.

The following are the query samples being developed to identifiy these issues. These are not yet implemented in the Pozi Connect application.

```
select property_pfi, '' as spi, propnum, 'R' as edit_code
from
(
select property_pfi, spi, propnum, count(*) num_parcels
from pc_vicmap_parcel vp
where
    multi_assessment = 'Y' and    
    propnum in ( select propnum from pc_vicmap_property_parcel_count where num_parcels > 1 ) and
    propnum in ( select propnum from pc_council_property_address ) and
    spi in ( select spi from pc_council_parcel ) and
    propnum not in ( select propnum from pc_council_property_parcel_count where num_parcels > 1 ) and    
    spi not in ( select spi from pc_council_parcel_property_count where num_props > 1 )    
group by spi
)
where num_parcels = 2
group by property_pfi

union

select '' as property_pfi, spi, propnum, 'P' as edit_code
from
(
select property_pfi, spi, propnum
from
(
select property_pfi, spi, propnum, count(*) num_parcels
from pc_vicmap_parcel vp
where
    multi_assessment = 'Y' and    
    propnum in ( select propnum from pc_vicmap_property_parcel_count where num_parcels > 1 ) and
    propnum in ( select propnum from pc_council_property_address ) and
    spi in ( select spi from pc_council_parcel ) and
    propnum not in ( select propnum from pc_council_property_parcel_count where num_parcels > 1 ) and    
    spi not in ( select spi from pc_council_parcel_property_count where num_props > 1 )    
group by spi
)
where num_parcels = 2
group by property_pfi
)
order by propnum, edit_code desc
```
---

```
select property_pfi, '' as spi, 'R' as edit_code, 'parcel ' || spi || ': removing propnum ' || propnum || ' from multi-assessment to match properly later' as comments
from
(
select property_pfi, spi, propnum, count(*) num_parcels
from pc_vicmap_parcel vp
where
    multi_assessment = 'Y' and    
    propnum in ( select propnum from pc_vicmap_property_parcel_count where num_parcels > 1 ) and
    propnum in ( select propnum from pc_council_property_address ) and
    spi in ( select spi from pc_council_parcel ) and
    propnum not in ( select propnum from pc_council_property_parcel_count where num_parcels > 1 ) and    
    spi not in ( select spi from pc_council_parcel_property_count where num_props > 1 )        
group by spi
)
where num_parcels = 2
group by property_pfi
```