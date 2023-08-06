SELECT t0.t_catsrcid
      ,t0.catsrcname
      ,t1.wm_catsrcid
      ,t2.wp_catsrcid
      ,t3.v_catsrcid
      ,t4.n_catsrcid
      ,t0.t_flux
      ,t1.wm_flux
      ,t2.wp_flux
      ,t3.v_flux
      ,t4.n_flux
      ,t0.t_flux_err
      ,t1.wm_flux_err
      ,t2.wp_flux_err
      ,t3.v_flux_err
      ,t4.n_flux_err
      ,t1.wm_assoc_distance_arcsec
      ,t1.wm_assoc_r
      ,t2.wp_assoc_distance_arcsec
      ,t2.wp_assoc_r
      ,t3.v_assoc_distance_arcsec
      ,t3.v_assoc_r
      ,t4.n_assoc_distance_arcsec
      ,t4.n_assoc_r
      ,t0.t_pa
      ,t0.t_major
      ,t0.t_minor
      ,t0.t_ra
      ,t0.t_decl
  FROM (SELECT c1.catsrcid AS t_catsrcid
              ,c1.catsrcname
              ,c1.ra AS t_ra
              ,c1.decl AS t_decl
              ,c1.i_int_avg AS t_flux
              ,c1.i_int_avg_err AS t_flux_err
              ,c1.pa AS t_pa
              ,c1.major AS t_major
              ,c1.minor AS t_minor
          FROM (SELECT catsrcid
                      ,catsrcname
                      ,ra
                      ,decl
                      ,pa
                      ,major
                      ,minor
                      ,i_int_avg
                      ,i_int_avg_err
                  FROM catalogedsources
                 WHERE cat_id = 7
                   AND zone BETWEEN CAST(FLOOR(CAST(%(decl_central)s AS DOUBLE) - %(fov_radius)s) AS INTEGER)
                                AND CAST(FLOOR(CAST(%(decl_central)s AS DOUBLE) + %(fov_radius)s) AS INTEGER)
                   AND decl BETWEEN CAST(%(decl_central)s AS DOUBLE) - %(fov_radius)s
                                AND CAST(%(decl_central)s AS DOUBLE) + %(fov_radius)s
                   AND ra BETWEEN CAST(%(ra_central)s AS DOUBLE) - alpha(%(fov_radius)s, %(decl_central)s)
                              AND CAST(%(ra_central)s AS DOUBLE) + alpha(%(fov_radius)s, %(decl_central)s)
                   AND x * COS(RADIANS(%(decl_central)s)) * COS(RADIANS(%(ra_central)s))
                     + y * COS(RADIANS(%(decl_central)s)) * SIN(RADIANS(%(ra_central)s))
                     + z * SIN(RADIANS(%(decl_central)s)) > COS(RADIANS(%(fov_radius)s))
               ) c1
       ) t0
       LEFT OUTER JOIN
       (SELECT c1.catsrcid AS t_catsrcid
              ,c2.catsrcid AS wm_catsrcid
              ,c2.i_int_avg AS wm_flux
              ,c2.i_int_avg_err AS wm_flux_err
              ,3600 * DEGREES(2 * ASIN(SQRT( (c1.x - c2.x) * (c1.x - c2.x)
                                           + (c1.y - c2.y) * (c1.y - c2.y)
                                           + (c1.z - c2.z) * (c1.z - c2.z)
                                           ) / 2)
                             ) AS wm_assoc_distance_arcsec
              ,SQRT(((c1.ra * COS(RADIANS(c1.decl)) - c2.ra * COS(RADIANS(c2.decl)))
                    * (c1.ra * COS(RADIANS(c1.decl)) - c2.ra * COS(RADIANS(c2.decl)))
                    / (c1.ra_err * c1.ra_err + c2.ra_err * c2.ra_err))
                    + ((c1.decl - c2.decl) * (c1.decl - c2.decl)
                    / (c1.decl_err * c1.decl_err + c2.decl_err * c2.decl_err))
                    ) AS wm_assoc_r
          FROM (SELECT catsrcid
                      ,ra
                      ,decl
                      ,ra_err
                      ,decl_err
                      ,x
                      ,y
                      ,z
                  FROM catalogedsources
                 WHERE cat_id = 7
                   AND zone BETWEEN CAST(FLOOR(CAST(%(decl_central)s AS DOUBLE) - %(fov_radius)s) AS INTEGER)
                                AND CAST(FLOOR(CAST(%(decl_central)s AS DOUBLE) + %(fov_radius)s) AS INTEGER)
                   AND decl BETWEEN CAST(%(decl_central)s AS DOUBLE) - %(fov_radius)s
                                AND CAST(%(decl_central)s AS DOUBLE) + %(fov_radius)s
                   AND ra BETWEEN CAST(%(ra_central)s AS DOUBLE) - alpha(%(fov_radius)s, %(decl_central)s)
                              AND CAST(%(ra_central)s AS DOUBLE) + alpha(%(fov_radius)s, %(decl_central)s)
                   AND x * COS(RADIANS(%(decl_central)s)) * COS(RADIANS(%(ra_central)s))
                     + y * COS(RADIANS(%(decl_central)s)) * SIN(RADIANS(%(ra_central)s))
                     + z * SIN(RADIANS(%(decl_central)s)) > COS(RADIANS(%(fov_radius)s))
               ) c1
              ,(SELECT catsrcid
                      ,zone
                      ,ra
                      ,decl
                      ,ra_err
                      ,decl_err
                      ,x
                      ,y
                      ,z
                      ,i_int_avg
                      ,i_int_avg_err
                  FROM catalogedsources
                 WHERE cat_id = 5
                   AND (src_type = 'S' OR src_type = 'M')
                   AND zone BETWEEN CAST(FLOOR(CAST(%(decl_central)s AS DOUBLE) - %(fov_radius)s) AS INTEGER)
                                AND CAST(FLOOR(CAST(%(decl_central)s AS DOUBLE) + %(fov_radius)s) AS INTEGER)
                   AND decl BETWEEN CAST(%(decl_central)s AS DOUBLE) - %(fov_radius)s
                                AND CAST(%(decl_central)s AS DOUBLE) + %(fov_radius)s
                   AND ra BETWEEN CAST(%(ra_central)s AS DOUBLE) - alpha(%(fov_radius)s, %(decl_central)s)
                              AND CAST(%(ra_central)s AS DOUBLE) + alpha(%(fov_radius)s, %(decl_central)s)
                   AND x * COS(RADIANS(%(decl_central)s)) * COS(RADIANS(%(ra_central)s))
                     + y * COS(RADIANS(%(decl_central)s)) * SIN(RADIANS(%(ra_central)s))
                     + z * SIN(RADIANS(%(decl_central)s)) > COS(RADIANS(%(fov_radius)s))
               ) c2
         WHERE /*c2.zone BETWEEN CAST(FLOOR(c1.decl - %(assoc_theta)s) AS INTEGER)
                           AND CAST(FLOOR(c1.decl + %(assoc_theta)s) AS INTEGER)
           AND*/ c2.decl BETWEEN c1.decl - %(assoc_theta)s
                           AND c1.decl + %(assoc_theta)s
           AND c2.ra BETWEEN c1.ra - alpha(%(assoc_theta)s, c1.decl)
                         AND c1.ra + alpha(%(assoc_theta)s, c1.decl)
           AND c2.x * c1.x + c2.y * c1.y + c2.z * c1.z > COS(RADIANS(%(assoc_theta)s))
           AND SQRT(((c2.ra * COS(RADIANS(c2.decl)) - c1.ra * COS(RADIANS(c1.decl)))
                    * (c2.ra * COS(RADIANS(c2.decl)) - c1.ra * COS(RADIANS(c1.decl)))
                    / (c2.ra_err * c2.ra_err + c1.ra_err * c1.ra_err))
                    + ((c2.decl - c1.decl) * (c2.decl - c1.decl)
                    / (c2.decl_err * c2.decl_err + c1.decl_err * c1.decl_err))) < %(deRuiter_reduced)s
       ) t1
    ON t0.t_catsrcid = t1.t_catsrcid
       LEFT OUTER JOIN
       (SELECT c1.catsrcid AS t_catsrcid
              ,c2.catsrcid AS wp_catsrcid
              ,c2.i_int_avg AS wp_flux
              ,c2.i_int_avg_err AS wp_flux_err
              ,3600 * DEGREES(2 * ASIN(SQRT( (c1.x - c2.x) * (c1.x - c2.x)
                                           + (c1.y - c2.y) * (c1.y - c2.y)
                                           + (c1.z - c2.z) * (c1.z - c2.z)
                                           ) / 2)
                             ) AS wp_assoc_distance_arcsec
              ,SQRT(((c1.ra * COS(RADIANS(c1.decl)) - c2.ra * COS(RADIANS(c2.decl)))
                    * (c1.ra * COS(RADIANS(c1.decl)) - c2.ra * COS(RADIANS(c2.decl)))
                    / (c1.ra_err * c1.ra_err + c2.ra_err * c2.ra_err))
                    + ((c1.decl - c2.decl) * (c1.decl - c2.decl)
                    / (c1.decl_err * c1.decl_err + c2.decl_err * c2.decl_err))
                    ) AS wp_assoc_r
          FROM (SELECT catsrcid
                      ,ra
                      ,decl
                      ,ra_err
                      ,decl_err
                      ,x
                      ,y
                      ,z
                  FROM catalogedsources
                 WHERE cat_id = 7
                   AND zone BETWEEN CAST(FLOOR(CAST(%(decl_central)s AS DOUBLE) - %(fov_radius)s) AS INTEGER)
                                AND CAST(FLOOR(CAST(%(decl_central)s AS DOUBLE) + %(fov_radius)s) AS INTEGER)
                   AND decl BETWEEN CAST(%(decl_central)s AS DOUBLE) - %(fov_radius)s
                                AND CAST(%(decl_central)s AS DOUBLE) + %(fov_radius)s
                   AND ra BETWEEN CAST(%(ra_central)s AS DOUBLE) - alpha(%(fov_radius)s, %(decl_central)s)
                              AND CAST(%(ra_central)s AS DOUBLE) + alpha(%(fov_radius)s, %(decl_central)s)
                   AND x * COS(RADIANS(%(decl_central)s)) * COS(RADIANS(%(ra_central)s))
                     + y * COS(RADIANS(%(decl_central)s)) * SIN(RADIANS(%(ra_central)s))
                     + z * SIN(RADIANS(%(decl_central)s)) > COS(RADIANS(%(fov_radius)s))
               ) c1
              ,(SELECT catsrcid
                      ,zone
                      ,ra
                      ,decl
                      ,ra_err
                      ,decl_err
                      ,x
                      ,y
                      ,z
                      ,i_int_avg
                      ,i_int_avg_err
                  FROM catalogedsources
                 WHERE cat_id = 6
                   AND (src_type = 'S' OR src_type = 'M')
                   AND zone BETWEEN CAST(FLOOR(CAST(%(decl_central)s AS DOUBLE) - %(fov_radius)s) AS INTEGER)
                                AND CAST(FLOOR(CAST(%(decl_central)s AS DOUBLE) + %(fov_radius)s) AS INTEGER)
                   AND decl BETWEEN CAST(%(decl_central)s AS DOUBLE) - %(fov_radius)s
                                AND CAST(%(decl_central)s AS DOUBLE) + %(fov_radius)s
                   AND ra BETWEEN CAST(%(ra_central)s AS DOUBLE) - alpha(%(fov_radius)s, %(decl_central)s)
                              AND CAST(%(ra_central)s AS DOUBLE) + alpha(%(fov_radius)s, %(decl_central)s)
                   AND x * COS(RADIANS(%(decl_central)s)) * COS(RADIANS(%(ra_central)s))
                     + y * COS(RADIANS(%(decl_central)s)) * SIN(RADIANS(%(ra_central)s))
                     + z * SIN(RADIANS(%(decl_central)s)) > COS(RADIANS(%(fov_radius)s))
               ) c2
         WHERE /*c2.zone BETWEEN CAST(FLOOR(c1.decl - %(assoc_theta)s) AS INTEGER)
                           AND CAST(FLOOR(c1.decl + %(assoc_theta)s) AS INTEGER)
           AND*/ c2.decl BETWEEN c1.decl - %(assoc_theta)s
                           AND c1.decl + %(assoc_theta)s
           AND c2.ra BETWEEN c1.ra - alpha(%(assoc_theta)s, c1.decl)
                         AND c1.ra + alpha(%(assoc_theta)s, c1.decl)
           AND c2.x * c1.x + c2.y * c1.y + c2.z * c1.z > COS(RADIANS(%(assoc_theta)s))
           AND SQRT(((c2.ra * COS(RADIANS(c2.decl)) - c1.ra * COS(RADIANS(c1.decl)))
                    * (c2.ra * COS(RADIANS(c2.decl)) - c1.ra * COS(RADIANS(c1.decl)))
                    / (c2.ra_err * c2.ra_err + c1.ra_err * c1.ra_err))
                    + ((c2.decl - c1.decl) * (c2.decl - c1.decl)
                    / (c2.decl_err * c2.decl_err + c1.decl_err * c1.decl_err))) < %(deRuiter_reduced)s
       ) t2
    ON t0.t_catsrcid = t2.t_catsrcid
       LEFT OUTER JOIN
       (SELECT c1.catsrcid AS t_catsrcid
              ,c2.catsrcid AS v_catsrcid
              ,c2.i_int_avg AS v_flux
              ,c2.i_int_avg_err AS v_flux_err
              ,3600 * DEGREES(2 * ASIN(SQRT( (c1.x - c2.x) * (c1.x - c2.x)
                                           + (c1.y - c2.y) * (c1.y - c2.y)
                                           + (c1.z - c2.z) * (c1.z - c2.z)
                                           ) / 2)
                             ) AS v_assoc_distance_arcsec
              ,SQRT(((c1.ra * COS(RADIANS(c1.decl)) - c2.ra * COS(RADIANS(c2.decl)))
                    * (c1.ra * COS(RADIANS(c1.decl)) - c2.ra * COS(RADIANS(c2.decl)))
                    / (c1.ra_err * c1.ra_err + c2.ra_err * c2.ra_err))
                    + ((c1.decl - c2.decl) * (c1.decl - c2.decl)
                    / (c1.decl_err * c1.decl_err + c2.decl_err * c2.decl_err))
                   ) AS v_assoc_r
          FROM (SELECT catsrcid
                      ,ra
                      ,decl
                      ,ra_err
                      ,decl_err
                      ,x
                      ,y
                      ,z
                  FROM catalogedsources
                 WHERE cat_id = 7
                   AND zone BETWEEN CAST(FLOOR(CAST(%(decl_central)s AS DOUBLE) - %(fov_radius)s) AS INTEGER)
                                AND CAST(FLOOR(CAST(%(decl_central)s AS DOUBLE) + %(fov_radius)s) AS INTEGER)
                   AND decl BETWEEN CAST(%(decl_central)s AS DOUBLE) - %(fov_radius)s
                                AND CAST(%(decl_central)s AS DOUBLE) + %(fov_radius)s
                   AND ra BETWEEN CAST(%(ra_central)s AS DOUBLE) - alpha(%(fov_radius)s, %(decl_central)s)
                              AND CAST(%(ra_central)s AS DOUBLE) + alpha(%(fov_radius)s, %(decl_central)s)
                   AND x * COS(RADIANS(%(decl_central)s)) * COS(RADIANS(%(ra_central)s))
                     + y * COS(RADIANS(%(decl_central)s)) * SIN(RADIANS(%(ra_central)s))
                     + z * SIN(RADIANS(%(decl_central)s)) > COS(RADIANS(%(fov_radius)s))
               ) c1
              ,(SELECT catsrcid
                      ,zone
                      ,ra
                      ,decl
                      ,ra_err
                      ,decl_err
                      ,x
                      ,y
                      ,z
                      ,i_int_avg
                      ,i_int_avg_err
                  FROM catalogedsources
                 WHERE cat_id = 4
                   AND zone BETWEEN CAST(FLOOR(CAST(%(decl_central)s AS DOUBLE) - %(fov_radius)s) AS INTEGER)
                                AND CAST(FLOOR(CAST(%(decl_central)s AS DOUBLE) + %(fov_radius)s) AS INTEGER)
                   AND decl BETWEEN CAST(%(decl_central)s AS DOUBLE) - %(fov_radius)s
                                AND CAST(%(decl_central)s AS DOUBLE) + %(fov_radius)s
                   AND ra BETWEEN CAST(%(ra_central)s AS DOUBLE) - alpha(%(fov_radius)s, %(decl_central)s)
                              AND CAST(%(ra_central)s AS DOUBLE) + alpha(%(fov_radius)s, %(decl_central)s)
                   AND x * COS(RADIANS(%(decl_central)s)) * COS(RADIANS(%(ra_central)s))
                     + y * COS(RADIANS(%(decl_central)s)) * SIN(RADIANS(%(ra_central)s))
                     + z * SIN(RADIANS(%(decl_central)s)) > COS(RADIANS(%(fov_radius)s))
               ) c2
         WHERE /*c2.zone BETWEEN CAST(FLOOR(c1.decl - %(assoc_theta)s) AS INTEGER)
                          AND CAST(FLOOR(c1.decl + %(assoc_theta)s) AS INTEGER)
           AND*/ c2.decl BETWEEN c1.decl - %(assoc_theta)s
                          AND c1.decl + %(assoc_theta)s
           AND c2.ra BETWEEN c1.ra - alpha(%(assoc_theta)s, c1.decl)
                         AND c1.ra + alpha(%(assoc_theta)s, c1.decl)
           AND c2.x * c1.x + c2.y * c1.y + c2.z * c1.z > COS(RADIANS(%(assoc_theta)s))
           AND SQRT(((c2.ra * COS(RADIANS(c2.decl)) - c1.ra * COS(RADIANS(c1.decl)))
                    * (c2.ra * COS(RADIANS(c2.decl)) - c1.ra * COS(RADIANS(c1.decl)))
                    / (c2.ra_err * c2.ra_err + c1.ra_err * c1.ra_err))
                    + ((c2.decl - c1.decl) * (c2.decl - c1.decl)
                    / (c2.decl_err * c2.decl_err + c1.decl_err * c1.decl_err))) < %(deRuiter_reduced)s
       ) t3
    ON t0.t_catsrcid = t3.t_catsrcid
       LEFT OUTER JOIN
       (SELECT c1.catsrcid AS t_catsrcid
              ,c2.catsrcid AS n_catsrcid
              ,c2.i_int_avg AS n_flux
              ,c2.i_int_avg_err AS n_flux_err
              ,3600 * DEGREES(2 * ASIN(SQRT( (c1.x - c2.x) * (c1.x - c2.x)
                                           + (c1.y - c2.y) * (c1.y - c2.y)
                                           + (c1.z - c2.z) * (c1.z - c2.z)
                                           ) / 2)
                             ) AS n_assoc_distance_arcsec
              ,SQRT(((c1.ra * COS(RADIANS(c1.decl)) - c2.ra * COS(RADIANS(c2.decl)))
                    * (c1.ra * COS(RADIANS(c1.decl)) - c2.ra * COS(RADIANS(c2.decl)))
                    / (c1.ra_err * c1.ra_err + c2.ra_err * c2.ra_err))
                    + ((c1.decl - c2.decl) * (c1.decl - c2.decl)
                    / (c1.decl_err * c1.decl_err + c2.decl_err * c2.decl_err))
                   ) AS n_assoc_r
          FROM (SELECT catsrcid
                      ,ra
                      ,decl
                      ,ra_err
                      ,decl_err
                      ,x
                      ,y
                      ,z
                  FROM catalogedsources
                 WHERE cat_id = 7
                   AND zone BETWEEN CAST(FLOOR(CAST(%(decl_central)s AS DOUBLE) - %(fov_radius)s) AS INTEGER)
                                AND CAST(FLOOR(CAST(%(decl_central)s AS DOUBLE) + %(fov_radius)s) AS INTEGER)
                   AND decl BETWEEN CAST(%(decl_central)s AS DOUBLE) - %(fov_radius)s
                                AND CAST(%(decl_central)s AS DOUBLE) + %(fov_radius)s
                   AND ra BETWEEN CAST(%(ra_central)s AS DOUBLE) - alpha(%(fov_radius)s, %(decl_central)s)
                              AND CAST(%(ra_central)s AS DOUBLE) + alpha(%(fov_radius)s, %(decl_central)s)
                   AND x * COS(RADIANS(%(decl_central)s)) * COS(RADIANS(%(ra_central)s))
                     + y * COS(RADIANS(%(decl_central)s)) * SIN(RADIANS(%(ra_central)s))
                     + z * SIN(RADIANS(%(decl_central)s)) > COS(RADIANS(%(fov_radius)s))
               ) c1
               ,(SELECT catsrcid
                      ,zone
                      ,ra
                      ,decl
                      ,ra_err
                      ,decl_err
                      ,x
                      ,y
                      ,z
                      ,i_int_avg
                      ,i_int_avg_err
                  FROM catalogedsources
                 WHERE cat_id = 3
                   AND zone BETWEEN CAST(FLOOR(CAST(%(decl_central)s AS DOUBLE) - %(fov_radius)s) AS INTEGER)
                                AND CAST(FLOOR(CAST(%(decl_central)s AS DOUBLE) + %(fov_radius)s) AS INTEGER)
                   AND decl BETWEEN CAST(%(decl_central)s AS DOUBLE) - %(fov_radius)s
                                AND CAST(%(decl_central)s AS DOUBLE) + %(fov_radius)s
                   AND ra BETWEEN CAST(%(ra_central)s AS DOUBLE) - alpha(%(fov_radius)s, %(decl_central)s)
                              AND CAST(%(ra_central)s AS DOUBLE) + alpha(%(fov_radius)s, %(decl_central)s)
                   AND x * COS(RADIANS(%(decl_central)s)) * COS(RADIANS(%(ra_central)s))
                     + y * COS(RADIANS(%(decl_central)s)) * SIN(RADIANS(%(ra_central)s))
                     + z * SIN(RADIANS(%(decl_central)s)) > COS(RADIANS(%(fov_radius)s))
               ) c2
         WHERE /*c2.zone BETWEEN CAST(FLOOR(c1.decl - %(assoc_theta)s) AS INTEGER)
                           AND CAST(FLOOR(c1.decl + %(assoc_theta)s) AS INTEGER)
           AND*/ c2.decl BETWEEN c1.decl - %(assoc_theta)s
                           AND c1.decl + %(assoc_theta)s
           AND c2.ra BETWEEN c1.ra - alpha(%(assoc_theta)s, c1.decl)
                         AND c1.ra + alpha(%(assoc_theta)s, c1.decl)
           AND c2.x * c1.x + c2.y * c1.y + c2.z * c1.z > COS(RADIANS(%(assoc_theta)s))
           AND SQRT(((c2.ra * COS(RADIANS(c2.decl)) - c1.ra * COS(RADIANS(c1.decl)))
                    * (c2.ra * COS(RADIANS(c2.decl)) - c1.ra * COS(RADIANS(c1.decl)))
                    / (c2.ra_err * c2.ra_err + c1.ra_err * c1.ra_err))
                    + ((c2.decl - c1.decl) * (c2.decl - c1.decl)
                    / (c2.decl_err * c2.decl_err + c1.decl_err * c1.decl_err))) < %(deRuiter_reduced)s
       ) t4
    ON t0.t_catsrcid = t4.t_catsrcid
 WHERE t0.t_flux >= %(tgss_flux_cutoff)s
ORDER BY t0.t_catsrcid
;
