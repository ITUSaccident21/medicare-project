import React, { useEffect, useState } from 'react';
import { getMedicineCabinet } from '../services/apiClient';

export const CabinetPage: React.FC = () => {
  const [drugs, setDrugs] = useState<any[]>([]);

  useEffect(() => {
    getMedicineCabinet().then(data => setDrugs(data));
  }, []);

  return (
    <div className="cabinet-page">
      <h2>F2 - Tủ Thuốc Cá Nhân & Gia Đình</h2>
      <ul>
        {drugs.map(drug => (
          <li key={drug.id}>
            <strong>{drug.brandName}</strong> ({drug.strength}) - Hoạt chất: {drug.activeIngredient}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CabinetPage;
